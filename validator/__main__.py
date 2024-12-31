"""Application entry point."""


from structlog import get_logger, stdlib


from .custom_logging import set_up_custom_logging

logger: stdlib.BoundLogger = get_logger()