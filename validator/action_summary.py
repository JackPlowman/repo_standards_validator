from json import dump
from os import environ
from pathlib import Path

from structlog import get_logger, stdlib

logger: stdlib.BoundLogger = get_logger()


def generate_action_summary(analysed_repositories: dict) -> None:
    """Generate the action summary.

    Args:
        analysed_repositories (dict): The analysed repositories.
    """
    if "GITHUB_STEP_SUMMARY" in environ:
        logger.debug("Running in GitHub Actions, generating action summary")
        with Path(environ["GITHUB_STEP_SUMMARY"]).open("w") as file:
            dump(analysed_repositories, file, indent=4)
    else:
        logger.debug(
            "Not running in GitHub Actions, skipping generating action summary"
        )
