from github import Repository as GitHubRepositoryType
from structlog import get_logger, stdlib

from .custom_types import Repository as AnalysedRepository

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

    logger.debug(
        "Repository details",
        secret_scanning_push_protection=secret_scanning_push_protection,
        secret_scanning=secret_scanning,
        dependabot_security_updates=dependabot_security_updates,
    )

    try:
        code_scanning_alerts = len(list(repository.get_code_scanning_alerts(state='open')))
    except Exception:
        logger.warning("Could not fetch code scanning alerts", repository=repository.full_name)
        code_scanning_alerts = 0

    try:
        security_warnings = repository.get_vulnerability_alert().totalCount
    except Exception:
        logger.warning("Could not fetch security warnings", repository=repository.full_name)
        security_warnings = 0

    logger.debug(
        "Repository security details",
        code_scanning_alerts=code_scanning_alerts,
        security_warnings=security_warnings,
    )

    return AnalysedRepository(
        name=repository.name,
        full_name=repository.full_name,
        repository_link=repository.html_url,
        secret_scanning_push_protection=status_to_bool(secret_scanning_push_protection),
        secret_scanning=status_to_bool(secret_scanning),
        dependabot_security_updates=status_to_bool(dependabot_security_updates),
        open_security_warnings=security_warnings,
        code_scanning_alerts=code_scanning_alerts,
    )


def status_to_bool(status: str) -> bool:
    """Convert a status string to a boolean."""
    return status == "enabled"
