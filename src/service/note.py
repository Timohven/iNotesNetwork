import os
from src.model.note import Note

if os.getenv("NOTE_UNIT_TEST"):
    from src.fake import note as data
    print('Fake data (service level)')
else:
    from src.data import note as data
    print('Data from DB (service level)')


def get_all() -> list[None]:
    return data.get_all()


def get_specific(title) -> Note | None:
    return data.get_specific(title)


def create(note: Note) -> Note:
    return data.create(note)


def modify(title: str, note: Note) -> Note:
    return data.modify(title, note)


def delete(title: str) -> bool:
    return data.delete(title)
