from src.model.note import Note


_notes = [
    Note(name="Note1",
         description="about FastAPI",
         type_of_source="book",
         source="FastAPI веб-разработка на Python.pdf",
         language="RU"),
    Note(name="Note2",
         description="about Pydantic",
         type_of_source="web",
         source="file:///C:/Books/Python/FastAPI%20%D0%B2%D0%B5%D0%B1-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0%20%D0%BD%D0%B0%20Python.pdf",
         language="RU"),
    Note(name="Note3",
         description="about Pydantic",
         type_of_source="web",
         source="None",
         language="RU")
]


def get_all() -> list[Note]:
    print(*_notes)
    return _notes


def get_specific(name: str) -> Note | None:
    # if name==None: print('Ok!')
    for _note in _notes:
        if _note.name == name:
            return _note
    return None


def create(note: Note) -> Note:
    _notes.append(note)
    return note


def modify(note: Note) -> Note:
    return note


def replace(note: Note) -> Note:
    return note


def delete(name: str):
    return None
