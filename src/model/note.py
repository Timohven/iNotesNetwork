from pydantic import BaseModel, HttpUrl, Field, validator
from fastapi import Form, UploadFile, File
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4


class Tag(BaseModel):
    tag_id: UUID = Field(default_factory=uuid4)
    name: str


class Note(BaseModel):
    note_id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    source_type: str
    source_link: Optional[HttpUrl] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    files: Optional[List[UploadFile]] = None

    # @validator('files', pre=True, each_item=True)
    # def filter_empty_files(cls, v):
    #     if v.filename == '' or v.size == 0:
    #         return None  # Удаляет пустые файлы
    #     return v

    @classmethod
    def as_form(
            cls,
            note_id: UUID = Form(default_factory=uuid4),
            title: str = Form(...),
            content: str = Form(...),
            source_type: str = Form(...),
            source_link: Optional[HttpUrl] = Form(None),
            created_at: datetime = Form(default_factory=datetime.now),
            updated_at: datetime = Form(default_factory=datetime.now),
            files: Optional[List[UploadFile]] = None
    ) -> "Note":
        # print(files)
        return cls(
            note_id=note_id,
            title=title,
            content=content,
            source_type=source_type,
            source_link=source_link,
            created_at=created_at,
            updated_at=updated_at,
            files=files
        )
