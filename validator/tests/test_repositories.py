from unittest.mock import MagicMock, patch

from validator.repositories import retrieve_repositories


@patch("validator.repositories.Github")
def test_retrieve_repositories(mock_github: MagicMock) -> None:
    # Arrange
    config = MagicMock()
    # Act
    result = retrieve_repositories(config)
    # Assert
    assert result == mock_github.return_value.search_repositories.return_value
    mock_github.assert_called_once_with(config.github_token)
    mock_github.return_value.search_repositories.assert_called_once_with(
        query=f"user:{config.repository_owner} archived:false is:public"
    )
