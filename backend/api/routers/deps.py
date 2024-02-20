import os
from typing import Annotated
from fastapi import Header, HTTPException, Depends

from api.config.settings import settings
from api.schemas import NoteSchema

def api_key_valid(x_api_key: str = Header(...)):
    if x_api_key is None:
        raise HTTPException(status_code=400, detail="API Key header missing")
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

ApiKeyDep = Annotated[bool, Depends(api_key_valid)]


def valid_note_input(note: NoteSchema):
    """
        Check if the note input is valid.
    """
    file_path = os.path.join(settings.vault_dir, note.title + ".md")
    normalized_path = os.path.normpath(file_path)
    if not normalized_path.startswith(settings.vault_dir):
        raise HTTPException(status_code=400, detail="Invalid title. Path traversal attack detected.")
    return note    

ValidNoteInput = Annotated[NoteSchema, Depends(valid_note_input)]