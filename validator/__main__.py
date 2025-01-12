"""Application entry point."""

from dataclasses import asdict
from json import dump
from pathlib import Path

from structlog import get_logger, stdlib

from .action_summary import generate_action_summary
from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .custom_types import AnalysedRepositories
from .repositories import retrieve_repositories
from .repository_checks import check_repository

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
    with Path("repositories.json").open("w") as file:
        dump(analysed_repositories, file, indent=4)
    generate_action_summary(analysed_repositories)
    logger.info(
        "Repositories analysed",
        repositories=analysed_repositories,
    )


if __name__ == "__main__":
    main()
