from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Repository:
    """A representation of a GitHub repository."""

    name: str
    full_name: str
    secret_scanning_push_protection: bool
    secret_scanning: bool
    dependabot_security_updates: bool


class AnalysedRepositories(TypedDict):
    """A representation of a repository with the required settings."""

    owner: str
    repositories: list[dict]  # List of dictionaries representing Repository
