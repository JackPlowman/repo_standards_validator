from git import Repo


def clone_repository(repository_name: str, repository_clone_url: str) -> None:
    """Clone the repository.

    Args:
        repository_name (str): The name
        repository_clone_url (str): The URL to clone the repository from.
    """
    Repo.clone_from(
        repository_clone_url, f"validator/cloned_repositories/{repository_name}"
    )
