from os import walk

COMMON_FILE_EXTENSIONS = ["", ".md", ".rst", ".txt"]


def find_file(directory: str, filename: str) -> bool:
    """Find a file in a directory and its subdirectories.

    Args:
        directory (str): The starting directory path to search in
        filename (str): The name of the file to find

    Returns:
        bool: True if the file is found, otherwise False
    """
    if search_for_file(directory, filename):
        return True
    filename_without_extension = filename.split(".")[0]
    files_to_check = [
        f"{filename_without_extension}{extension}"
        for extension in COMMON_FILE_EXTENSIONS
    ]
    for filename_with_extension in files_to_check:
        if search_for_file(directory, filename_with_extension):
            return True
    return False


def search_for_file(directory: str, filename: str) -> bool:
    """Recursively search for a file in a directory and its subdirectories.

    Search uses case-insensitive matching.

    Args:
        directory (str): The directory to search in
        filename (str): The name of the file to find

    Returns:
        bool: True if the file is found, otherwise False
    """
    filename_lower = filename.lower()
    for _root, _dir, files in walk(directory):
        if any(f.lower() == filename_lower for f in files):
            return True
    return False
