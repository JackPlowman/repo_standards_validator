from validator.file import find_file_recursive


def test_find_file_recursive() -> None:
    # Arrange
    directory = "validator/tests"
    filename = "test_file.py"
    # Act
    result = find_file_recursive(directory, filename)
    # Assert
    assert result is True
