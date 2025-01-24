from github import Repository as GitHubRepositoryType
from structlog import get_logger, stdlib

from .custom_types import Repository as AnalysedRepository
from .file import find_file_recursive

logger: stdlib.BoundLogger = get_logger()


def check_repository(repository: GitHubRepositoryType) -> AnalysedRepository:
    """Check the repository for the required settings.

    Args:
        repository (GitHubRepositoryType): The repository to check.

    Returns:
        AnalysedRepository: The repository with the required settings.
    """
    logger.info("Checking repository", repository=repository.full_name)
    secret_scanning_push_protection = (
        repository.security_and_analysis.secret_scanning_push_protection.status
    )
    secret_scanning = repository.security_and_analysis.secret_scanning.status
    dependabot_security_updates = (
        repository.security_and_analysis.dependabot_security_updates.status
    )
    has_security_policy = find_file_recursive(
        f"validator/cloned_repositories/{repository.name}", "SECURITY.md"
    )
    logger.debug(
        "Repository details",
        secret_scanning_push_protection=secret_scanning_push_protection,
        secret_scanning=secret_scanning,
        dependabot_security_updates=dependabot_security_updates,
        has_security_policy=has_security_policy,
    )
    return AnalysedRepository(
        name=repository.name,
        full_name=repository.full_name,
        repository_link=repository.html_url,
        secret_scanning_push_protection=status_to_bool(secret_scanning_push_protection),
        secret_scanning=status_to_bool(secret_scanning),
        dependabot_security_updates=status_to_bool(dependabot_security_updates),
        has_security_policy=has_security_policy,
    )


def status_to_bool(status: str) -> bool:
    """Convert a status string to a boolean."""
    return status == "enabled"
