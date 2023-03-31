from fastapi import APIRouter, status
from manticore.analytics.mock_model.mock_model import MockModel
from manticore.workers.generic_api import get_processor


mock_model_router = APIRouter()


@mock_model_router.get('/processed_items', status_code=status.HTTP_200_OK)
async def processed_items():
    processor = get_processor()
    model = processor.models[MockModel.get_type()]
    return model.processed_items
