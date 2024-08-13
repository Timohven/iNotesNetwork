import os
# import src.fake.note as data
from src.model.note import Note
if os.getenv("NOTE_UNIT_TEST"):
    from src.fake import note as data
    print('Fake data (service level)')
else:
    from src.data import note as data
    print('Data from DB (service level)')


def get_all() -> list[None]:
    return data.get_all()


def get_specific(name) -> Note | None:
    return data.get_specific(name)


def create(note: Note) -> Note:
    return data.create(note)


def modify(name: str, note: Note) -> Note:
    return data.modify(name, note)


def delete(name: str) -> bool:
    return data.delete(name)
