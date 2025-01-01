from ..repository_checks import check_repository, status_to_bool

import pytest


def test_check_repository() -> None:
    # Arrange
    class MockRepository:
        def __init__(
            self,
            secret_scanning_push_protection,
            secret_scanning,
            dependabot_security_updates,
        ):
            self.security_and_analysis = MockSecurityAndAnalysis(
                secret_scanning_push_protection,
                secret_scanning,
                dependabot_security_updates,
            )
            self.name = "test-repo"
            self.full_name = "owner/test-repo"

    class MockSecurityAndAnalysis:
        def __init__(
            self,
            secret_scanning_push_protection,
            secret_scanning,
            dependabot_security_updates,
        ):
            self.secret_scanning_push_protection = MockStatus(
                secret_scanning_push_protection
            )
            self.secret_scanning = MockStatus(secret_scanning)
            self.dependabot_security_updates = MockStatus(dependabot_security_updates)

    class MockStatus:
        def __init__(self, status):
            self.status = status

    repository = MockRepository("enabled", "enabled", "enabled")
    # Act
    analysed_repository = check_repository(repository)
    # Assert
    assert analysed_repository.name == "test-repo"
    assert analysed_repository.full_name == "owner/test-repo"
    assert analysed_repository.secret_scanning_push_protection is True
    assert analysed_repository.secret_scanning is True
    assert analysed_repository.dependabot_security_updates is True


@pytest.mark.parametrize(
    "status, expected",
    [
        ("enabled", True),
        ("disabled", False),
        ("other", False),
    ],
)
def test_status_to_bool(status: str, expected: bool) -> None:
    # Act
    result = status_to_bool(status)
    # Assert
    assert result == expected
