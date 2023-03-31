from fastapi import APIRouter, status
from manticore.workers.generic_api import get_processor


processing_engine_router = APIRouter()


@processing_engine_router.get('/models', status_code=status.HTTP_200_OK)
async def models():
    processor = get_processor()
    return {
        'models': tuple(processor.models.keys())
    }
