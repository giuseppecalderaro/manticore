from fastapi import APIRouter, status
from manticore.components.sources.file_source.file_source import FileSource
from manticore.workers.generic_api import get_processor


file_source_router = APIRouter()


# Sequence Number
@file_source_router.get('/sequence_number', status_code=status.HTTP_200_OK)
async def sequence_number():
    processor = get_processor()
    source = processor.sources[FileSource.get_type()]
    return source.sequence_number
