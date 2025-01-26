from validator.custom_types import AnalysedRepositories, Repository
from validator.custom_types import RepositoryHasFiles, RepositorySecurityDetails

def test_repository() -> None:
    # Act
    repo = Repository(
        name="test-repo",
        full_name="owner/test-repo",
        repository_link="https://github.com/JackPlowman/repo_standards_validator",
        repository_security_details=RepositorySecurityDetails(
            secret_scanning_push_protection=True,
            secret_scanning=True,
            dependabot_security_updates=True,
            private_vulnerability_disclosures=True,
            code_scanning_alerts=5,
        ),
        repository_has_files=RepositoryHasFiles(
            has_security_policy=True,
            has_code_of_conduct=True,
            has_contributing=True,
            has_readme=True,
            has_project_technologies=True,
            has_license=True,
        ),
    )
    # Assert
    assert repo.name == "test-repo"
    assert repo.full_name == "owner/test-repo"
    assert (
        repo.repository_link
        == "https://github.com/JackPlowman/repo_standards_validator"
    )
    assert repo.repository_security_details == RepositorySecurityDetails(
        secret_scanning_push_protection=True,
        secret_scanning=True,
        dependabot_security_updates=True,
        private_vulnerability_disclosures=True,
        code_scanning_alerts=5,
    )
    assert repo.repository_has_files == RepositoryHasFiles(
        has_security_policy=True,
        has_code_of_conduct=True,
        has_contributing=True,
        has_readme=True,
        has_project_technologies=True,
        has_license=True,
    )


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
