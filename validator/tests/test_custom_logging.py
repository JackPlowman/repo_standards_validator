from unittest.mock import MagicMock, patch

from validator.custom_logging import set_up_custom_logging

FILE_PATH = "validator.custom_logging"


@patch(f"{FILE_PATH}.make_filtering_bound_logger")
@patch(f"{FILE_PATH}.configure")
def test_set_up_custom_logging(
    mock_configure: MagicMock, mock_make_filtering_bound_logger: MagicMock
) -> None:
    # Act
    set_up_custom_logging()
    # Assert
    mock_configure.assert_called_once_with(
        wrapper_class=mock_make_filtering_bound_logger.return_value
    )
