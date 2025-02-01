from github import Repository as GitHubRepositoryType
from structlog import get_logger, stdlib

from .custom_types import Repository as AnalysedRepository
from .custom_types import (
    RepositoryDetails,
    RepositoryKeyFiles,
    RepositorySecurityDetails,
)
from .file import find_file

logger: stdlib.BoundLogger = get_logger()


def check_repository(repository: GitHubRepositoryType) -> AnalysedRepository:
    """Check the repository for the required settings.

    Args:
        repository (GitHubRepositoryType): The repository to check.

    Returns:
        AnalysedRepository: The repository with the required settings.
    """
    logger.info("Checking repository", repository=repository.full_name)
    repository_details = check_repository_details(repository)
    repository_security_details = check_repository_security_details(repository)
    repository_key_files = check_repository_has_key_files(repository)
    logger.debug(
        "Repository checked",
        repository=repository.full_name,
        repository_details=repository_details,
        repository_security_details=repository_security_details,
        repository_key_files=repository_key_files,
    )
    return AnalysedRepository(
        name=repository.name,
        full_name=repository.full_name,
        repository_link=repository.html_url,
        repository_details=repository_details,
        repository_security_details=repository_security_details,
        repository_key_files=repository_key_files,
    )


def status_to_bool(status: str) -> bool:
    """Convert a status string to a boolean."""
    return status == "enabled"


def check_repository_details(repository: GitHubRepositoryType) -> RepositoryDetails:
    """Check the repository for the required details.

    Args:
        repository (p): The repository to check.

    Returns:
        RepositoryDetails: The repository with the required details.
    """
    open_pull_requests = len(
        [pull for pull in repository.get_pulls() if pull.state == "open"]
    )
    open_issues = len(
        [issue for issue in repository.get_issues() if issue.state == "open"]
    )
    return RepositoryDetails(
        open_pull_requests=open_pull_requests, open_issues=open_issues
    )


def check_repository_security_details(
    repository: GitHubRepositoryType,
) -> RepositorySecurityDetails:
    """Check the repository for the required security details.

    Args:
        repository (GitHubRepositoryType): The repository to check.

    Returns:
        RepositorySecurityDetails: The repository with the required security details.
    """
    secret_scanning_push_protection = (
        repository.security_and_analysis.secret_scanning_push_protection.status
    )
    secret_scanning = repository.security_and_analysis.secret_scanning.status
    dependabot_security_updates = (
        repository.security_and_analysis.dependabot_security_updates.status
    )
    private_vulnerability_disclosures = repository.get_vulnerability_alert()
    code_scanning_alerts = get_code_scanning_alerts(repository)
    return RepositorySecurityDetails(
        secret_scanning_push_protection=status_to_bool(secret_scanning_push_protection),
        secret_scanning=status_to_bool(secret_scanning),
        dependabot_security_updates=status_to_bool(dependabot_security_updates),
        private_vulnerability_disclosures=private_vulnerability_disclosures,
        code_scanning_alerts=code_scanning_alerts,
    )


def check_repository_has_key_files(
    repository: GitHubRepositoryType,
) -> RepositoryKeyFiles:
    """Check if the repository has the required key files.

    Args:
        repository (GitHubRepositoryType): The repository to check.

    Returns:
        RepositoryKeyFiles: The repository with the required files.
    """
    repository_directory = f"validator/cloned_repositories/{repository.name}"
    has_security_policy = find_file(repository_directory, "SECURITY.md")
    has_code_of_conduct = find_file(repository_directory, "CODE_OF_CONDUCT.md")
    has_contributing = find_file(repository_directory, "CONTRIBUTING.md")
    has_readme = find_file(repository_directory, "README.md")
    has_project_technologies = find_file(
        repository_directory, "PROJECT_TECHNOLOGIES.md"
    )
    has_license = find_file(repository_directory, "LICENSE")
    return RepositoryKeyFiles(
        has_security_policy=has_security_policy,
        has_code_of_conduct=has_code_of_conduct,
        has_contributing=has_contributing,
        has_readme=has_readme,
        has_project_technologies=has_project_technologies,
        has_license=has_license,
    )


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
