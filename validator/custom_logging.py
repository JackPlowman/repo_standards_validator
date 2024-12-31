from logging import DEBUG, INFO
from os import getenv

from structlog import configure, get_logger, make_filtering_bound_logger, stdlib

logger: stdlib.BoundLogger = get_logger()


def set_up_custom_logging() -> None:
<<<<<<< HEAD
    """Set up custom logging for the application."""
=======
    """Setup custom logging for the application."""
>>>>>>> 8e389e9 (update)
    level = INFO
    if getenv("INPUT_DEBUG", "false").lower() == "true":
        level = DEBUG
    configure(wrapper_class=make_filtering_bound_logger(level))