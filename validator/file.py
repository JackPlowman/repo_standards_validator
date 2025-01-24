from os import walk


def find_file_recursive(directory: str, filename: str) -> bool:
    """Recursively search for a file in a directory and its subdirectories.

    Search uses case-insensitive matching.

    Args:
        directory (str): The starting directory path to search in
        filename (str): The name of the file to find

    Returns:
        bool: The path to the file if found, otherwise False
    """
    filename_lower = filename.lower()
    for _root, _dirs, files in walk(directory):
        for file in files:
            if file.lower() == filename_lower:
                return True
    return False
