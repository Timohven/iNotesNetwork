from pydantic import BaseModel
from fastapi import Form
# from typing import List, Optional


class Note(BaseModel):
    name: str
    description: str
    type_of_source: str
    source: str
    language: str

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            description: str = Form(...),
            type_of_source: str = Form(...),
            source: str = Form(...),
            language: str = Form(...),
    ) -> "Note":
        return cls(name=name, description=description, type_of_source=type_of_source, source=source, language=language)