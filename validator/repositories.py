from __future__ import annotations

from typing import TYPE_CHECKING

from github import Github
from structlog import get_logger, stdlib

if TYPE_CHECKING:
    from collections.abc import Iterable

    from github.Repository import Repository

    from .configuration import Configuration

logger: stdlib.BoundLogger = get_logger()


def retrieve_repositories(configuration: Configuration) -> Iterable[Repository]:
    """Retrieve the list of repositories to analyse.

    Returns:
        Iterable[Repository]: The list of repositories.
    """
    github = Github(configuration.github_token)
    repositories = github.search_repositories(
        query=f"user:{configuration.repository_owner} archived:false is:public"
    )
    logger.info(
        "Retrieved repositories to analyse",
        repositories_count=repositories.totalCount,
        repositories=[repository.full_name for repository in repositories],
    )
    return repositories
