from typing import Any
import datetime
import os
import aiobotocore
import aiofiles
from botocore.signers import CloudFrontSigner
import ciso8601
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from manticore.config.config import Config
from manticore.utils.logger import Logger
from manticore.utils.time_utils import delta_us, timestamp_to_datetime
from manticore.utils.utils import content_type


class S3Storage:
    @staticmethod
    def is_expired(presigned_url: str) -> bool:
        """
        This method checks whether a presigned url is expired or not.
        :param presigned_url: s3 presigned url
        :return: bool
        """
        expired = True
        if not presigned_url:
            Logger().debug('No presigned url')
            return expired

        params = presigned_url.split('?')[1].split('&')
        created_on = None
        expires_in = None
        for param in params:
            if "X-Amz-Date" in param:
                created_on = ciso8601.parse_datetime(param.split('=')[1]).replace(tzinfo=None)
            if "X-Amz-Expires" in param:
                expires_in = int(param.split('=')[1])

        if created_on and expires_in:
            Logger().debug(f'Parsed created_on {created_on} and expires_in {expires_in}')
            expires_on = created_on + datetime.timedelta(seconds=expires_in)
            expired = delta_us(datetime.datetime.utcnow(), expires_on) >= 0

        Logger().debug(f'is_expired returning {expired}')
        return expired

    def __init__(self, name: str, cfg: Config):
        self._session = aiobotocore.get_session()
        self._profile_name = cfg.get(name, 'profile')
        self._bucket_name = cfg.get(name, 'bucket_name')
        self._region_name = cfg.get(name, 'region_name')
        self._aws_access_key_id = cfg.get(name, 'aws_access_key_id')
        self._aws_secret_access_key = cfg.get(name, 'aws_secret_access_key')
        self._expiry = cfg.get(name, 'expiry')
        self._key_pem = cfg.get(name, 'key_pem')
        self._key_id = cfg.get(name, 'key_id')
        self._cloudfront_base_url = cfg.get(name, 'cloudfront_base_url')
        self._signer = None

    async def init(self) -> bool:
        self._signer = CloudFrontSigner(self._key_id, self.rsa_signer)
        return True

    @property
    def expiry(self):
        return self._expiry

    def rsa_signer(self, message):
        with open(self._key_pem, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    async def get_one(self, key: str) -> Any:
        async with self._session.create_client('s3',
                                               region_name=self._region_name,
                                               aws_secret_access_key=self._aws_secret_access_key,
                                               aws_access_key_id=self._aws_access_key_id) as client:
            return await client.get_object(Bucket=self._bucket_name, Key=key)

    async def insert_one(self, key: str, data: Any, access_control_list: str = 'private') -> bool:
        async with self._session.create_client('s3',
                                               region_name=self._region_name,
                                               aws_secret_access_key=self._aws_secret_access_key,
                                               aws_access_key_id=self._aws_access_key_id) as client:
            res = await client.put_object(Bucket=self._bucket_name,
                                          Key=key,
                                          Body=data,
                                          ContentType=content_type(key),
                                          ACL=access_control_list)
            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True

            return False

    async def delete_one(self, key) -> bool:
        async with self._session.create_client('s3',
                                               region_name=self._region_name,
                                               aws_secret_access_key=self._aws_secret_access_key,
                                               aws_access_key_id=self._aws_access_key_id) as client:
            res = await client.delete_object(Bucket=self._bucket_name, Key=key)
            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True

            return False

    async def get_url(self, key: str, expires_in: int) -> Any:
        content_disposition = f'attachment; filename={key};'
        params = {
            'Bucket': self._bucket_name,
            'Key': key,
            'ResponseContentDisposition': content_disposition
            }

        async with self._session.create_client('s3',
                                               region_name=self._region_name,
                                               aws_secret_access_key=self._aws_secret_access_key,
                                               aws_access_key_id=self._aws_access_key_id) as client:
            presigned_url = await client.generate_presigned_url('get_object',
                                                                Params=params,
                                                                ExpiresIn=expires_in)
            Logger().debug(f'get_url() returning {presigned_url}')
            return presigned_url

    async def upload_directory(self, path: str, access_control_list: str = 'private'):
        # root, dirs, files
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                async with aiofiles.open(file_path, mode='rb') as filedesc:
                    content = await filedesc.read()
                    if not await self.insert_one(file_path, content, access_control_list):
                        return False

        return True

    async def validate_cloudfront_url(self, url: str) -> bool:
        if url:
            url_parts = url.split('?')
            params = url_parts[1].split('&')
            for param in params:
                key, value = param.split('=')
                if key == "Expires":
                    expiry = timestamp_to_datetime(int(value)).date()
                    if expiry > datetime.date.today():
                        Logger().debug('Cloudfront URL is valid, returning')
                        return True

        Logger().debug(f'Cloudfron URL {url} is not valid or expired')
        return False

    async def get_cloudfront_url(self, name: str, expiry_date: datetime.date) -> str:
        signed_url = self._signer.generate_presigned_url(f'{self._cloudfront_base_url}/{name}',
                                                         date_less_than=expiry_date)
        Logger().debug(f'Generated cloudfront url: {signed_url}')
        return signed_url
