from unittest.mock import MagicMock, patch, call

from validator.__main__ import main, clean_up

FILE_PATH = "validator.__main__"


@patch(f"{FILE_PATH}.set_up_custom_logging")
@patch(f"{FILE_PATH}.Configuration")
@patch(f"{FILE_PATH}.clean_up")
@patch(f"{FILE_PATH}.retrieve_repositories")
@patch(f"{FILE_PATH}.clone_repository")
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
    mock_clone_repository: MagicMock,
    mock_retrieve_repositories: MagicMock,
    mock_clean_up: MagicMock,
    mock_configuration: MagicMock,
    mock_set_up_custom_logging: MagicMock,
) -> None:
    # Act
    main()
    # Assert
    mock_set_up_custom_logging.assert_called_once()
    mock_clean_up.assert_has_calls([call(), call()])
    mock_configuration.assert_called_once_with()
    mock_retrieve_repositories.assert_called_once_with(mock_configuration.return_value)
    mock_clone_repository.assert_not_called()
    mock_dump.assert_called_once()
    mock_generate_action_summary.assert_called_once()
    mock_path.assert_called_once_with("repositories.json")
    mock_analysed_repositories.assert_called_once_with(
        owner=mock_configuration.return_value.repository_owner,
        repositories=[],
    )
    mock_asdict.assert_not_called()
@patch(f"{FILE_PATH}.Path")
@patch(f"{FILE_PATH}.rmtree")
def test_clean_up(
    mock_rmtree: MagicMock,
    mock_path: MagicMock,
) -> None:
    # Arrange
    mock_path.return_value.iterdir.return_value = [
        MagicMock(is_dir=lambda: True),
        MagicMock(is_dir=lambda: False),
    ]
    # Act
    clean_up()
    # Assert
    mock_path.assert_called_once_with("validator/cloned_repositories")
    mock_path.return_value.iterdir.assert_called_once()
    mock_rmtree.assert_called_once_with(mock_path.return_value.iterdir.return_value[0])
