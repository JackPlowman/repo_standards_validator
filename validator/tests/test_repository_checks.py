from unittest.mock import MagicMock

import pytest

from validator.repository_checks import check_repository, status_to_bool


def test_check_repository() -> None:
    # Arrange
    repository = MagicMock(
        secret_scanning_push_protection="enabled",  # noqa: S106
        secret_scanning="enabled",  # noqa: S106
        dependabot_security_updates="enabled",
    )
    # Act
    analysed_repository = check_repository(repository)
    # Assert
    assert analysed_repository.name == "test-repo"
    assert analysed_repository.full_name == "owner/test-repo"
    assert analysed_repository.secret_scanning_push_protection is True
    assert analysed_repository.secret_scanning is True
    assert analysed_repository.dependabot_security_updates is True


@pytest.mark.parametrize(
    ("status", "expected"),
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
