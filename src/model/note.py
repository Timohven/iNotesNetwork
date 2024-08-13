from pydantic import BaseModel


class Note(BaseModel):
    name: str
    description: str
    type_of_source: str
    source: str
    language: str
