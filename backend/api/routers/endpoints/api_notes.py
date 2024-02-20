import os

from fastapi import APIRouter
from api.config.settings import settings

router = APIRouter()

ignore_dirs_full_paths = {os.path.join(settings.vault_dir, ignore_dir) for ignore_dir in settings.ignore_dirs}

def should_ignore_dir(dir_path: str) -> bool:
    """
    Check if dir_path or any of its parent directories should be ignored.
    """
    global ignore_dirs_full_paths
    parts = dir_path.split(os.sep)
    for i in range(1, len(parts) + 1):
        if os.sep.join(parts[:i]) in ignore_dirs_full_paths:
            return True
    return False


@router.get("/")
async def list_notes() -> list[str]:
    """
        Iterates over all files in the notes directory and subdirectories and returns a list of their filenames.
    """
    file_paths = []
    for root, _, files in os.walk(settings.vault_dir):
        # Check if current directory should be ignored
        if should_ignore_dir(root):
            continue
        for file in files:
            # Construct the full file path relative to the root directory
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, settings.vault_dir)
            file_paths.append(relative_path)
    return file_paths
        

