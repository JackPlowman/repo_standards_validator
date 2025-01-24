from validator.custom_types import AnalysedRepositories, Repository


def test_repository() -> None:
    # Act
    repo = Repository(
        name="test-repo",
        full_name="owner/test-repo",
        repository_link="https://github.com/JackPlowman/repo_standards_validator",
        secret_scanning_push_protection=True,
        secret_scanning=True,
        dependabot_security_updates=True,
        has_security_policy=True,
        has_code_of_conduct=True,
        has_contributing=True,
        has_readme=True,
        has_project_technologies=True,
    )
    # Assert
    assert repo.name == "test-repo"
    assert repo.full_name == "owner/test-repo"
    assert (
        repo.repository_link
        == "https://github.com/JackPlowman/repo_standards_validator"
    )
    assert repo.secret_scanning_push_protection is True
    assert repo.secret_scanning is True
    assert repo.dependabot_security_updates is True
    assert repo.has_security_policy is True
    assert repo.has_code_of_conduct is True
    assert repo.has_contributing is True
    assert repo.has_readme is True
    assert repo.has_project_technologies is True


def test_analysed_repositories() -> None:
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
