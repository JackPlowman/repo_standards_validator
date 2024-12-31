"""Application entry point."""

from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .repositories import retrieve_repositories
from .repository_checks import check_repository

logger: stdlib.BoundLogger = get_logger()


def main() -> None:
    """Application entry point."""
    set_up_custom_logging()
    configuration = Configuration()
    repositories = retrieve_repositories(configuration)
    analysed_repositories = []
    for repository in repositories:
        analysed_repository = check_repository(repository)
        analysed_repositories.append(analysed_repository)
    logger.info(
        "Repositories analysed",
        repositories=analysed_repositories,
    )


if __name__ == "__main__":
    main()
