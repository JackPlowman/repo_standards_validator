from unittest.mock import MagicMock

import pytest

from validator.repository_checks import (
    check_repository,
    get_code_scanning_alerts,
    status_to_bool,
)


def test_check_repository() -> None:
    # Arrange
    configuration = MagicMock()
    repository = MagicMock()
    repository.name = "test-repo"
    repository.full_name = "owner/test-repo"
    repository.security_and_analysis.secret_scanning_push_protection.status = "enabled"
    repository.security_and_analysis.secret_scanning.status = "enabled"
    repository.security_and_analysis.dependabot_security_updates.status = "enabled"
    # Act
    analysed_repository = check_repository(configuration, repository)
    # Assert
    assert analysed_repository.name == "test-repo"
    assert analysed_repository.full_name == "owner/test-repo"


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


@pytest.mark.parametrize(
    ("alerts", "count"),
    [
        (
            MagicMock(
                totalCount=5,
                __iter__=lambda _self: iter(
                    [
                        MagicMock(state="open"),
                        MagicMock(state="open"),
                        MagicMock(state="open"),
                        MagicMock(state="open"),
                        MagicMock(state="open"),
                        MagicMock(state="closed"),
                    ]
                ),
            ),
            5,
        ),
        (
            MagicMock(
                totalCount=0,
                __iter__=lambda _self: iter([]),
            ),
            0,
        ),
    ],
)
def test_get_code_scanning_alerts(alerts: MagicMock, count: int) -> None:
    # Arrange
    repository = MagicMock()
    repository.get_codescan_alerts.return_value = alerts
    # Act
    result = get_code_scanning_alerts(repository)
    # Assert
    assert result == count


def test_get_code_scanning_alerts__exception() -> None:
    # Arrange
    repository = MagicMock()
    repository.get_codescan_alerts.side_effect = Exception
    # Act
    result = get_code_scanning_alerts(repository)
    # Assert
    assert result == 0
