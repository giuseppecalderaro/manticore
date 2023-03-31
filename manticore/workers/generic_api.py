from typing import Optional
import asyncio
from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, PositiveInt
from manticore.entry_point import initialise_logger, cfg
from manticore.workers.processors_factory import ProcessorsFactory


processor_api = FastAPI()
processor_router = APIRouter()


@processor_api.on_event('startup')
async def startup():
    initialise_logger(cfg)

    processor = ProcessorsFactory.make(cfg.processor_name, cfg.class_name, cfg)
    loop = asyncio.get_event_loop()
    active = await processor.core(loop)
    if not active:
        raise RuntimeError(f'{cfg.processor_name} is NOT active.')

    setattr(processor_api, 'processor_instance', processor)


def get_processor():
    return getattr(processor_api, 'processor_instance')


### Processor
# Info
@processor_api.get('/info', status_code=status.HTTP_200_OK, tags=['Processor'])
async def processor_info():
    processor = get_processor()
    return {
        'name': processor.name,
        'type': processor.get_type(),
        'version': processor.version,
        'sources': tuple(processor.sources.keys()),
        'sinks': tuple(processor.sinks.keys())
    }

# Shutdown
class ProcessorShutdownSerialiser(BaseModel):
    magic_code: str = Field(...)

@processor_api.post('/shutdown', status_code=status.HTTP_200_OK, tags=['Processor'])
async def processor_shutdown(request: ProcessorShutdownSerialiser):
    if request.magic_code == '0xDEADBEEF':
        loop = asyncio.get_event_loop()
        loop.stop()
        return 'OK'

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong magic code')

# Task Timeout
class TaskTimeoutSerialiser(BaseModel):
    task_timeout: Optional[PositiveInt] = Field(...)

@processor_router.post('/task_timeout', status_code=status.HTTP_200_OK)
async def task_timeout(request: TaskTimeoutSerialiser):
    processor = get_processor()
    processor.task_timeout = request.task_timeout
    return 'OK'
