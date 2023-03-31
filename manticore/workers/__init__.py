### Factory
from manticore.workers.processors_factory import ProcessorsFactory
from manticore.workers.runner.runner import Runner
from manticore.workers.processing_engine.processing_engine import ProcessingEngine

### Runner processor
ProcessorsFactory.register(Runner)

### ProcessingEngine processor
ProcessorsFactory.register(ProcessingEngine)
