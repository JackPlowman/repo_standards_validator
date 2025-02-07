"""Application entry point."""

from dataclasses import asdict
from json import dump
from pathlib import Path
from shutil import rmtree

from structlog import get_logger, stdlib

from .action_summary import generate_action_summary
from .configuration import Configuration
from .custom_logging import set_up_custom_logging
from .custom_types import AnalysedRepositories
from .git_actions import clone_repository
from .repositories import retrieve_repositories
from .repository_checks import check_repository

logger: stdlib.BoundLogger = get_logger()


def main() -> None:
    """Application entry point."""
    set_up_custom_logging()
    clean_up()
    configuration = Configuration()
    repositories = retrieve_repositories(configuration)
    raw_analysed_repositories = []
    total_repositories = repositories.totalCount
    for index, repository in enumerate(repositories, 1):
        clone_repository(repository.name, repository.clone_url)
        analysed_repository = check_repository(configuration, repository)
        raw_analysed_repositories.append(asdict(analysed_repository))
        logger.info(
            "Repository analysed",
            repository=analysed_repository.full_name,
            percentage_complete=f"{int(index / total_repositories * 100)}%",
        )
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
    clean_up()


def clean_up() -> None:
    """Clean up the cloned repositories."""
    logger.debug("Cleaning up cloned repositories")
    cloned_repositories = Path("validator/cloned_repositories")
    for repository in cloned_repositories.iterdir():
        if repository.is_dir():
            rmtree(repository)


if __name__ == "__main__":
    main()
