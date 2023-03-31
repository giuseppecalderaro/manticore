from setuptools import setup, find_namespace_packages


with open('README.md', 'r') as fd:
    long_description = fd.read()


install_requires = [
    'aiofiles',
    'aiokafka',
    'aioredis',
    'ciso8601',
    'cryptography',
    'fastapi',
    'loguru',
    'multimethod',
    'numpy',
    'orjson',
    'protobuf',
    'pycapnp',
    'pyzmq',
    'uuid',
    'uvicorn',

    # SQLAlchemy
    "SQLAlchemy",
    "SQLAlchemy-Utils",
    "zope.sqlalchemy",
    "psycopg2-binary",
    "transaction",

    # Mongo
    "motor",

    # S3
    "aiobotocore"
]


tests_require = [
    'pytest',
    'pytest-cov'
]


dev_require = [
    'ipdb',
    'line-profiler'
]


setup_kwargs = {
    'name': 'manticore',
    'version': '1.0.0',
    'author': 'Giuseppe Calderaro',
    'author_email': 'giuseppecalderaro@gmail.com',
    'description': (
        'Core library'
    ),
    'long_description': long_description,
    'url': '',
    'packages': find_namespace_packages(),
    'python_requires': '>=3.8',
    'classifiers': [
        'Programming Language :: Python :: 3.8'
    ],
    'install_requires': install_requires,
    'tests_require': tests_require
}


setup(**setup_kwargs)
