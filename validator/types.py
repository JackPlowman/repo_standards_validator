from dataclasses import dataclass


@dataclass
class Repository:
    """A representation of a repository."""

    name: str
    full_name: str
    secret_scanning_push_protection: bool
    secret_scanning: bool
    dependabot_security_updates: bool
