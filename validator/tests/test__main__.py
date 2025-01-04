from ..__main__ import main
from unittest.mock import patch, MagicMock
FILE_PATH = "validator.__main__"

@patch(f"{FILE_PATH}.set_up_custom_logging")
@patch(f"{FILE_PATH}.Configuration")
@patch(f"{FILE_PATH}.retrieve_repositories")
@patch(f"{FILE_PATH}.check_repository")
@patch(f"{FILE_PATH}.asdict")
@patch(f"{FILE_PATH}.AnalysedRepositories")
@patch(f"{FILE_PATH}.Path")
@patch(f"{FILE_PATH}.dump")
@patch(f"{FILE_PATH}.generate_action_summary")
def test_main(
    mock_generate_action_summary: MagicMock,
    mock_dump: MagicMock,
    mock_path: MagicMock,
    mock_analysed_repositories: MagicMock,
    mock_asdict: MagicMock,
    mock_check_repository: MagicMock,
    mock_retrieve_repositories: MagicMock,
    mock_configuration: MagicMock,
    mock_set_up_custom_logging: MagicMock,
) -> None:
    # Act
    main()
    # Assert
    mock_set_up_custom_logging.assert_called_once()
    mock_configuration.assert_called_once_with()
    mock_retrieve_repositories.assert_called_once_with(mock_configuration.return_value)
    mock_dump.assert_called_once()
    mock_generate_action_summary.assert_called_once()
    mock_path.assert_called_once_with("repositories.json")
    mock_analysed_repositories.assert_called_once_with(
        owner=mock_configuration.return_value.repository_owner,
        repositories=[],
    )
    mock_asdict.assert_not_called()
