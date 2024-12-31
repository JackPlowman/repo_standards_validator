"""Application entry point."""


from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .repositories import retrieve_repositories

logger: stdlib.BoundLogger = get_logger()

def main() -> None:
    """Application entry point."""
    set_up_custom_logging()
    configuration = Configuration()
    _repositories = retrieve_repositories(configuration)

if __name__ == "__main__":
    main()
