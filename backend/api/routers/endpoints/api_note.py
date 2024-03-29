import os
from fastapi import APIRouter, HTTPException
from api.config.settings import settings
from api.routers import deps
from api import schemas

router = APIRouter()

@router.put("/")
async def create_note(
    note: deps.ValidNoteInput,
) -> schemas.MessageSchema:
    """
        Create a new markdown note in the vault directory.
    """
    file_path = os.path.join(settings.vault_dir, note.title + ".md")
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Note with this title already exists.")
    with open(file_path, "w") as file:
        file.write(note.content)
    return {"message": "Note created successfully."}


@router.patch("/")
async def append_to_note(
    note: deps.ValidNoteInput,
) -> schemas.MessageSchema:
    """
        Append content to an existing markdown note in the vault directory.
    """
    file_path = os.path.join(settings.vault_dir, note.title + ".md")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Note with this title does not exist.")
    with open(file_path, "a") as file:
        file.write('\n' + note.content)
    return {"message": "Content appended to note successfully."}