from typing import Any, cast, Dict, Optional, Tuple
import asyncio
import signal
import sys
import traceback
from manticore.config.config import Config
from manticore.components.sinks.sinks_factory import SinksFactory
from manticore.components.sources.sources_factory import SourcesFactory
from manticore.interfaces.processor import Processor
from manticore.interfaces.source import Source
from manticore.objects.generic_object import Package
from manticore.utils.logger import Logger
from manticore.utils.system import check_system_is_linux
from manticore.utils.utils import init_content_type


class GenericProcessor(Processor):
    @staticmethod
    def _exception_handler(loop, context) -> None:
        loop.default_exception_handler(context)
        key = 'exception'
        if key not in context:
            key = 'message'
        Logger().critical(f'*** EXCEPTION: {context[key]}')
        loop.error_encountered = True
        loop.stop()

    @staticmethod
    def _sigterm_handler(loop) -> None:
        Logger().info('*** SIGTERM: Gracefully terminating process')
        loop.stop()

    @staticmethod
    def validate_filters(filters: Dict[str, Any],
                         mandatory_keys: Dict[str, Any],
                         optional_keys: Dict[str, Any]) -> Tuple[bool, str]:
        if not mandatory_keys:
            mandatory_keys = {}

        if not optional_keys:
            optional_keys = {}

        for key in mandatory_keys:
            if key not in filters:
                detail = f'Mandatory key {key} not present in filters'
                Logger().error(detail)
                return False, detail

            if not isinstance(filters[key], mandatory_keys[key]):
                detail = f'Mandatory key {key} not of the right type'
                Logger().error(detail)
                return False, detail

        for key in filters:
            if key in mandatory_keys:
                continue

            if key not in optional_keys:
                detail = f'Filter key {key} is not a valid optional key'
                Logger().error(detail)
                return False, detail

            if not isinstance(filters[key], optional_keys[key]):
                detail = f'Filter key {key} is not of the right type'
                Logger().debug(detail)
                return False, detail

        detail = 'OK'
        return True, detail

    def __init__(self, processor_name: str, cfg: Config):
        self._name = processor_name
        self._version = cfg.get('General', 'version')
        self._config = cfg
        self._active = False
        self._processing = False
        self.sources = {}
        self.sinks = {}
        self._uvloop_enabled = cfg.get(processor_name, 'uvloop_enabled')
        self.task_timeout = cfg.get(processor_name, 'task_timeout')
        self._enable_log_queue_sizes = cfg.get(processor_name, 'enable_log_queue_sizes')
        self._strict_exceptions = cfg.get(processor_name, 'strict_exceptions')
        self._active_tasks = 0

        # We print the config in the logfile as soon as possible.
        # Useful for debugging
        Logger().info('*** CONFIGURATION ***')
        Logger().info(cfg.properties)
        Logger().info('*** *** ***')

        # There's no timelord here

        # Queues
        self._in_q = cast(asyncio.Queue, None)
        self._in_q_threshold = cfg.get(processor_name, 'in_queue_threshold')

        self._out_q = cast(asyncio.Queue, None)
        self._out_q_threshold = cfg.get(processor_name, 'out_queue_threshold')
        #

        source_names = cfg.get(processor_name, 'sources')
        for source_name in source_names:
            source_type = cfg.get(source_name, 'type')
            self.sources[source_name] = SourcesFactory.make(source_name, source_type, cfg)

        sink_names = cfg.get(processor_name, 'sinks')
        for sink_name in sink_names:
            sink_type = cfg.get(sink_name, 'type')
            self.sinks[sink_name] = SinksFactory.make(sink_name, sink_type, cfg)

        # Initialise content analyser
        init_content_type()

        # Initialise interface
        from manticore.workers.generic_api import processor_api, processor_router
        processor_api.include_router(processor_router, prefix=f'/{self.name}', tags=[self.name])

    @property
    def config(self) -> Config:
        return self._config

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def active(self) -> bool:
        return self._active

    async def _log_queue_sizes(self) -> None:
        while True:
            if self._in_q:
                Logger().info(f'In queue count: {self._in_q.qsize()}')
            if self._out_q:
                Logger().info(f'Out queue count: {self._out_q.qsize()}')
            await asyncio.sleep(30)

    def _is_any_source_valid(self) -> bool:
        return self._active_tasks > 2

    def _create_task(self, func: Any, name: str) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(func, name=name)
        self._active_tasks += 1

    def _destroy_task(self) -> bool:
        self._active_tasks -= 1
        if self._active_tasks == 0:
            asyncio.get_event_loop().stop()
            return False

        return True

    async def _add_obj_to_input_queue(self, source: Source, obj: Optional[Package]) -> bool:
        if not source.valid:
            Logger().info(f'_input_task {source.name} quitting')
            self._destroy_task()
            return False

        if not obj:
            return True

        await self._in_q.put(obj)

        if self._in_q_threshold and self._in_q.qsize() > self._in_q_threshold:
            Logger().debug(f'''Throttling: in_q ({self._in_q.qsize()}) > '''
                           '''threshold {self._in_q_threshold}''')
            await self._in_q.join()

        return True

    async def _generator_input_task(self, source: Source) -> None:
        try:
            async for obj in source.recv():
                if not await self._add_obj_to_input_queue(source, obj):
                    return
        except Exception:
            traceback.print_exc(file=sys.stdout)
            if self._strict_exceptions:
                raise

    async def _input_task(self, source: Source) -> None:
        while True:
            try:
                obj = await source.recv()
            except Exception:
                traceback.print_exc(file=sys.stdout)
                if self._strict_exceptions:
                    raise

            if not await self._add_obj_to_input_queue(source, obj):
                return

    async def _processing_task(self) -> None:
        while True:
            try:
                obj = await asyncio.wait_for(self._in_q.get(), timeout=self.task_timeout)
            except asyncio.TimeoutError:
                if not self._is_any_source_valid():
                    Logger().info('_processing_task quitting')
                    self._destroy_task()
                    return

                Logger().debug('_processing_task timeout')
                continue

            try:
                await self.process(obj)
            except Exception:
                traceback.print_exc(file=sys.stdout)
                if self._strict_exceptions:
                    raise

            if self._out_q_threshold and self._out_q.qsize() > self._out_q_threshold:
                Logger().debug(f'''Throttling: out_q ({self._out_q.qsize()}) > '''
                               '''threshold {self._out_q_threshold}''')
                await self._out_q.join()

            self._in_q.task_done()

    async def _output_task(self) -> None:
        while True:
            try:
                obj = await asyncio.wait_for(self._out_q.get(), timeout=self.task_timeout)
            except asyncio.TimeoutError:
                if not self._is_any_source_valid():
                    Logger().info('_output_task quitting')
                    self._destroy_task()
                    return

                Logger().debug('_output_task timeout')
                continue

            try:
                coros = [sink.send(obj) for sink in self.sinks.values() if sink.should_send(obj)]
                await asyncio.gather(*coros, return_exceptions=False)
            except Exception:
                traceback.print_exc(file=sys.stdout)
                if self._strict_exceptions:
                    raise

            self._out_q.task_done()

    async def inject(self, obj: Package) -> None:
        await self._in_q.put(obj)

    async def init(self) -> bool:
        Logger().info(f'{self.__class__.__name__} initializing')

        for _, source in self.sources.items():
            if await source.init():
                Logger().info('Successfully logged in to ' + source.name)
            else:
                Logger().info(f'Logging in {source.name} failed')
                raise RuntimeError(f'Cannot initialise source {source.name}')

        for _, sink in self.sinks.items():
            Logger().info(f'Initialising {sink.name}')
            if await sink.init():
                Logger().info('Done')
            else:
                Logger().error('Failed')
                return self._active

        if self._enable_log_queue_sizes:
            asyncio.create_task(self._log_queue_sizes())

        self._active = True
        return self._active

    async def core(self, loop) -> bool:
        active = await self.init()
        if not active:
            return False

        # Async Queues
        self._in_q = asyncio.Queue()
        self._out_q = asyncio.Queue()

        for source in self.sources.values():
            if source.is_generator:
                self._create_task(self._generator_input_task(source), name=source.name)
            else:
                self._create_task(self._input_task(source), name=source.name)

        self._create_task(self._processing_task(), 'ProcessingTask')
        self._create_task(self._output_task(), 'OutputTask')
        return True

    def run(self) -> bool:
        Logger().info(f'{self._name} starting')

        if self._uvloop_enabled:
            import uvloop
            loop = uvloop.new_event_loop()
            asyncio.set_event_loop(loop)
            print('Using uvLoop')
            Logger().info('Using uvLoop')
        else:
            loop = asyncio.get_event_loop()

        setattr(loop, 'error_encountered', False)
        loop.set_exception_handler(GenericProcessor._exception_handler)

        if check_system_is_linux():
            loop.add_signal_handler(signal.SIGTERM, self._sigterm_handler, loop)

        try:
            active = loop.run_until_complete(self.core(loop))
            if not active:
                raise RuntimeError(f'{self._name} is NOT active.')

            loop.run_forever()
        except KeyboardInterrupt:
            Logger().debug('Requested keyboard interruption')
        except asyncio.CancelledError:
            Logger().debug('Cancelled error')
        finally:
            Logger().info(f'{self._name} stopping')

            try:
                for task in asyncio.all_tasks():
                    task.cancel()
            except RuntimeError:
                pass

            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        if loop.error_encountered:
            Logger().error(f'Loop quit with errors')
            return False

        Logger().info('Bye')
        return True
