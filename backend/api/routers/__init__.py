from fastapi import APIRouter, Depends
from .endpoints import api_notes, api_note
from . import deps

api_router = APIRouter(prefix="/api", dependencies=[Depends(deps.api_key_valid)])

api_router.include_router(api_notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(api_note.router, prefix="/note", tags=["note"])