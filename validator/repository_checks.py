from github import Repository as GitHubRepositoryType
from structlog import get_logger, stdlib

from .custom_types import Repository as AnalysedRepository
from .file import find_file

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
    code_scanning_alerts = get_code_scanning_alerts(repository)
    has_security_policy = find_file(repository_directory, "SECURITY.md")
    has_code_of_conduct = find_file(repository_directory, "CODE_OF_CONDUCT.md")
    has_contributing = find_file(repository_directory, "CONTRIBUTING.md")
    has_readme = find_file(repository_directory, "README.md")
    has_project_technologies = find_file(
        repository_directory, "PROJECT_TECHNOLOGIES.md"
    )
    has_license = find_file(repository_directory, "LICENSE")

    logger.debug(
        "Repository details",
        secret_scanning_push_protection=secret_scanning_push_protection,
        secret_scanning=secret_scanning,
        dependabot_security_updates=dependabot_security_updates,
        code_scanning_alerts=code_scanning_alerts,
        has_security_policy=has_security_policy,
        has_code_of_conduct=has_code_of_conduct,
        has_contributing=has_contributing,
        has_readme=has_readme,
        has_project_technologies=has_project_technologies,
        has_license=has_license,
    )

    return AnalysedRepository(
        name=repository.name,
        full_name=repository.full_name,
        repository_link=repository.html_url,
        secret_scanning_push_protection=status_to_bool(secret_scanning_push_protection),
        secret_scanning=status_to_bool(secret_scanning),
        dependabot_security_updates=status_to_bool(dependabot_security_updates),
        code_scanning_alerts=code_scanning_alerts,
        has_security_policy=has_security_policy,
        has_code_of_conduct=has_code_of_conduct,
        has_contributing=has_contributing,
        has_readme=has_readme,
        has_project_technologies=has_project_technologies,
        has_license=has_license,
    )


def status_to_bool(status: str) -> bool:
    """Convert a status string to a boolean."""
    return status == "enabled"


def get_code_scanning_alerts(repository: GitHubRepositoryType) -> int:
    """Get the number of open code scanning alerts for a repository.

    Args:
        repository (GitHubRepositoryType): The repository to get the code scanning
        alerts for.

    Returns:
        int: The number of open code scanning alerts.
    """
    try:
        paginated_alerts = repository.get_codescan_alerts()
        logger.debug(
            "Retrieving code scanning alerts", total=paginated_alerts.totalCount
        )
        return len([alert for alert in paginated_alerts if alert.state == "open"])
    except Exception:
        logger.exception(
            "Could not fetch code scanning alerts", repository=repository.full_name
        )
        return 0
