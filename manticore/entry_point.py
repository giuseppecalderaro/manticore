from typing import List
import os
import sys
from uvicorn import run
from manticore.config.config import Config
from manticore.utils.logger import Logger
from manticore.workers.processors_factory import ProcessorsFactory


def usage() -> None:
    print('Usage: \n'
          './main.py <main class> <config file>')


def initialise_logger(config: Config) -> str:
    from manticore.workers.generic_api import processor_api
    log_file_path = config.get(config.processor_name, 'log_file_path') or config.get('General', 'log_file_path')
    log_level = config.get(config.processor_name, 'log_level') or config.get('General', 'log_level')
    processor_api.logger = Logger.make_logger(log_file_path, log_level)
    return log_level


def main(_: int, __: List[str]) -> bool:
    # Initialise api
    enable_api = cfg.get(cfg.processor_name, 'enable_api')

    if enable_api:
        # Start processor
        reload_api = cfg.get(cfg.processor_name, 'reload')
        server_host = cfg.get(cfg.processor_name, 'server_host')
        server_port = int(cfg.get(cfg.processor_name, 'server_port'))

        try:
            log_level = cfg.get(cfg.processor_name, 'log_level') or cfg.get('General', 'log_level')

            run('manticore.workers.generic_api:processor_api',
                host=server_host,
                port=server_port,
                log_level=log_level,
                reload=reload_api)
            return True
        except RuntimeError:
            print(f'{cfg.processor_name} stopping')
            return False
    else:
        initialise_logger(cfg)
        main_class = ProcessorsFactory.make(cfg.processor_name, cfg.class_name, cfg)
        return main_class.run()


if len(sys.argv) != 3:
    usage()
    sys.exit(os.EX_USAGE)

cfg = Config(sys.argv[1], sys.argv[2])
