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
    repository_directory = f"validator/cloned_repositories/{repository.name}"
    logger.info("Checking repository", repository=repository.full_name)
    secret_scanning_push_protection = (
        repository.security_and_analysis.secret_scanning_push_protection.status
    )
    secret_scanning = repository.security_and_analysis.secret_scanning.status
    dependabot_security_updates = (
        repository.security_and_analysis.dependabot_security_updates.status
    )
    has_security_policy = find_file_recursive(repository_directory, "SECURITY.md")
    has_code_of_conduct = find_file_recursive(
        repository_directory, "CODE_OF_CONDUCT.md"
    )
    has_contributing = find_file_recursive(repository_directory, "CONTRIBUTING.md")
    has_readme = find_file_recursive(repository_directory, "README.md")
    has_project_technologies = find_file_recursive(
        repository_directory, "PROJECT_TECHNOLOGIES.md"
    )
    logger.debug(
        "Repository details",
        secret_scanning_push_protection=secret_scanning_push_protection,
        secret_scanning=secret_scanning,
        dependabot_security_updates=dependabot_security_updates,
        has_security_policy=has_security_policy,
        has_code_of_conduct=has_code_of_conduct,
        has_contributing=has_contributing,
        has_readme=has_readme,
        has_project_technologies=has_project_technologies,
    )
    return AnalysedRepository(
        name=repository.name,
        full_name=repository.full_name,
        repository_link=repository.html_url,
        secret_scanning_push_protection=status_to_bool(secret_scanning_push_protection),
        secret_scanning=status_to_bool(secret_scanning),
        dependabot_security_updates=status_to_bool(dependabot_security_updates),
        has_security_policy=has_security_policy,
        has_code_of_conduct=has_code_of_conduct,
        has_contributing=has_contributing,
        has_readme=has_readme,
        has_project_technologies=has_project_technologies,
    )


def status_to_bool(status: str) -> bool:
    """Convert a status string to a boolean."""
    return status == "enabled"
