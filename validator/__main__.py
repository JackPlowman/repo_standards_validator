"""Application entry point."""


from structlog import get_logger, stdlib


from .custom_logging import set_up_custom_logging

logger: stdlib.BoundLogger = get_logger()

def main() -> None:
    """Application entry point."""
    set_up_custom_logging()
    logger.info("Hello, World!")

if __name__ == "__main__":
    main()
