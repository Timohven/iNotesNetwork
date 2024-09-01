from src.model.note import Note, Tag
from src.error import Missing, Duplicate
from datetime import datetime
import uuid

_tags = [
    Tag(tag_id=str(uuid.uuid4()),
        name="python"),
    Tag(tag_id=str(uuid.uuid4()),
        name="fastapi"),
    Tag(tag_id=str(uuid.uuid4()),
        name="django"),
]
_notes = [
    Note(note_id=str(uuid.uuid4()),
         title="Note1",
         content="about FastAPI",
         source_type="web",
         source_link="https://example1.com",
         created_at=datetime.now(),
         updated_at=datetime.now(),
         files=[])
         # tags=[
         #    Tag(name="python"),
         #    Tag(name="fastapi")])
]


def get_all() -> list[Note]:
    print(*_notes)
    return _notes


def get_specific(title: str) -> Note | None:
    for _note in _notes:
        if _note.title == title:
            return _note
    #     else:
    #         raise Missing(msg=f"Note '{title}' not found")
    # return None
    raise Missing(msg=f"Note '{title}' not found")
    return None


def create(note: Note) -> Note:
    # note.note_id = uuid.uuid4()
    # note.created_at = datetime.now()
    # note.updated_at = datetime.now()
    _notes.append(note)
    return note


def modify(note: Note) -> Note:
    return note


def replace(note: Note) -> Note:
    return note


def delete(title: str):
    return None
