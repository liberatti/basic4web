import inspect
import logging
import os

import basic4web.config as base_config


class CustomLogger(logging.Logger):
    def info(self, msg, *args, **kwargs):
        frame = inspect.currentframe().f_back
        caller_method = frame.f_code.co_name
        filename = os.path.basename(frame.f_globals.get("__file__", ""))
        lineno = frame.f_lineno
        super().info(f"[{filename}][{caller_method}][{lineno}] {msg}", *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        frame = inspect.currentframe().f_back
        caller_method = frame.f_code.co_name
        filename = os.path.basename(frame.f_globals.get("__file__", ""))
        lineno = frame.f_lineno
        super().error(f"[{filename}][{caller_method}][{lineno}] {msg}", *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        frame = inspect.currentframe().f_back
        caller_method = frame.f_code.co_name
        filename = os.path.basename(frame.f_globals.get("__file__", ""))
        lineno = frame.f_lineno
        super().warning(
            f"[{filename}][{caller_method}][{lineno}] {msg}", *args, **kwargs
        )


logger = CustomLogger(__name__)

level = getattr(logging, base_config.get("LOG_LEVEL"), logging.INFO)
logger.setLevel(level)
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
formatter = logging.Formatter(
    f"%(asctime)s - %(process)d/%(thread)d - {base_config.get('CORE_VERSION')} - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
