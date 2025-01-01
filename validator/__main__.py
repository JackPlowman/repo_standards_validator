"""Application entry point."""

from structlog import get_logger, stdlib

from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .repositories import retrieve_repositories
from .repository_checks import check_repository
from .types import AnalysedRepositories
from json import dump
from dataclasses import asdict
from .action_summary import generate_action_summary
logger: stdlib.BoundLogger = get_logger()


def main() -> None:
    """Application entry point."""
    set_up_custom_logging()
    configuration = Configuration()
    repositories = retrieve_repositories(configuration)
    raw_analysed_repositories = []
    for repository in repositories:
        analysed_repository = check_repository(repository)
        raw_analysed_repositories.append(asdict(analysed_repository))
    analysed_repositories = AnalysedRepositories(
        owner=configuration.repository_owner, repositories=raw_analysed_repositories
    )
    with open("repositories.json", "w") as file:
        dump(analysed_repositories, file, indent=4)
    generate_action_summary(analysed_repositories)
    logger.info(
        "Repositories analysed",
        repositories=analysed_repositories,
    )


if __name__ == "__main__":
    main()
