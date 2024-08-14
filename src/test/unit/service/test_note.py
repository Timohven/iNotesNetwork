import sys
sys.path.insert(0, '../iNotesNetwork')
from src.model.note import Note
from src.service import note as code

sample = Note(name="Note14",
              description="about FastAPI new version",
              type_of_source="book",
              source="FastAPI веб-разработка на Python.pdf",
              language="RU")


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_specific("Note14")
    assert resp == sample


def test_get_missing():
    resp = code.get_specific("Non-existent note")
    assert resp is None
