from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    content: str
