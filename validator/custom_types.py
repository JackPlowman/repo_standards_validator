from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Repository:
    """A representation of a GitHub repository."""

    name: str
    full_name: str
    repository_link: str
    secret_scanning_push_protection: bool
    secret_scanning: bool
    dependabot_security_updates: bool
    open_security_warnings: int
    code_scanning_alerts: int

class AnalysedRepositories(TypedDict):
    """A representation of a repository with the required settings."""

    owner: str
    repositories: list[dict]  # List of dictionaries representing Repository
