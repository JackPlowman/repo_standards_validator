from os import walk


def find_file_recursive(directory: str, filename: str) -> bool:
    """Recursively search for a file in a directory and its subdirectories.

    Search uses case-insensitive matching.

    Args:
        directory (str): The starting directory path to search in
        filename (str): The name of the file to find

    Returns:
        bool: True if the file is found, otherwise False
    """
    filename_lower = filename.lower()
    for _root, _dir, files in walk(directory):
        if any(f.lower() == filename_lower for f in files):
            return True
    return False
