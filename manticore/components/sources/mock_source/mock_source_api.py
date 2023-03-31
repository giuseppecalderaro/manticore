from typing import Optional
from fastapi import APIRouter, status
from pydantic import BaseModel, Field, PositiveInt
from manticore.components.sources.mock_source.mock_source import MockSource
from manticore.objects.objects_factory import ObjectsFactory
from manticore.objects.normalised.mock import MockV1, MockV2
import manticore.utils.time_utils as tutil
from manticore.workers.generic_api import get_processor


mock_source_router = APIRouter()


# Sleep time
class SleepTimeSerialiser(BaseModel):
    sleep_time: Optional[PositiveInt] = Field(...)

@mock_source_router.post('/sleep_time', status_code=status.HTTP_200_OK)
async def sleep_time(request: SleepTimeSerialiser):
    processor = get_processor()
    source = processor.sources[MockSource.get_type()]
    source.sleep_time = request.sleep_time
    return 'OK'

# Inject
@mock_source_router.post('/inject_v1', status_code=status.HTTP_200_OK)
async def inject_v1():
    processor = get_processor()
    obj = MockV1.build('MOCK_ID', tutil.now_us(), 'MockData')
    pkg = ObjectsFactory.make_package(obj, 'MockSource', 'MockDestination')
    await processor.inject(pkg)
    return 'OK'

@mock_source_router.post('/inject_v2', status_code=status.HTTP_200_OK)
async def inject_v2():
    processor = get_processor()
    obj = MockV2.build('MOCK_ID', tutil.now_us(), 'MockData', 'MockData2')
    pkg = ObjectsFactory.make_package(obj, 'MockSource', 'MockDestination')
    await processor.inject(pkg)
    return 'OK'
