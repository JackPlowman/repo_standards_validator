from validator.file import find_file


def test_find_file() -> None:
    # Arrange
    directory = "validator/tests"
    filename = "test_file.py"
    # Act
    result = find_file(directory, filename)
    # Assert
    assert result is True
