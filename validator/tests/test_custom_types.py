from validator.custom_types import AnalysedRepositories, Repository


def test_repository() -> None:
    # Act
    repo = Repository(
        name="test-repo",
        full_name="owner/test-repo",
        secret_scanning_push_protection=True,
        secret_scanning=True,
        dependabot_security_updates=True,
    )
    # Assert
    assert repo.name == "test-repo"
    assert repo.full_name == "owner/test-repo"
    assert repo.secret_scanning_push_protection is True
    assert repo.secret_scanning is True
    assert repo.dependabot_security_updates is True


def test_analysed_repositories_() -> None:
    # Arrange
    repos = [
        {
            "name": "test-repo",
            "full_name": "owner/test-repo",
            "secret_scanning_push_protection": True,
            "secret_scanning": True,
            "dependabot_security_updates": True,
        }
    ]
    # Act
    analysed = AnalysedRepositories(owner="owner", repositories=repos)
    # Assert
    assert analysed["owner"] == "owner"
    assert len(analysed["repositories"]) == 1
    assert analysed["repositories"][0]["name"] == "test-repo"
