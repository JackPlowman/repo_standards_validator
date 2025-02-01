from dataclasses import dataclass
from typing import TypedDict


@dataclass
class RepositorySecurityDetails:
    """A representation of a GitHub repository's security details."""

    secret_scanning_push_protection: bool
    secret_scanning: bool
    dependabot_security_updates: bool
    private_vulnerability_disclosures: bool
    code_scanning_alerts: int


@dataclass
class RepositoryHasFiles:
    """A representation of a GitHub repository's key files."""

    has_security_policy: bool
    has_code_of_conduct: bool
    has_contributing: bool
    has_readme: bool
    has_project_technologies: bool
    has_license: bool


@dataclass
class RepositoryDetails:
    """A representation of a GitHub repository's details."""

    open_pull_requests: int
    open_issues: int


@dataclass
class Repository:
    """A representation of a GitHub repository."""

    name: str
    full_name: str
    repository_link: str
    repository_details: RepositoryDetails
    repository_security_details: RepositorySecurityDetails
    repository_key_files: RepositoryHasFiles


class AnalysedRepositories(TypedDict):
    """A representation of a repository with the required settings."""

    owner: str
    repositories: list[Repository]
