import os
import pytest
import sys
sys.path.insert(0, '../iNotesNetwork')
from src.model.note import Note
from src.error import Missing, Duplicate

# set this before data imports below for data.init
os.environ["NOTE_SQLITE_DB"] = ":memory:"
from src.data import note


@pytest.fixture
def sample() -> Note:
    return Note(name="Note20",
                description="about FastAPI new version",
                type_of_source="book",
                source="FastAPI веб-разработка на Python.pdf",
                language="RU")


def test_create(sample):
    resp = note.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = note.create(sample)


def test_get_one(sample):
    resp = note.get_specific(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = note.get_specific("boxturtle")


def test_modify(sample):
    note.language = "UKR"
    resp = note.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Note = Note(name="snurfle",
                       description="about Flask",
                       type_of_source="web",
                       source="https://flask.palletsprojects.com/en/3.0.x/",
                       language="EN")
    with pytest.raises(Missing):
        _ = note.modify(thing.name, thing)


def test_delete(sample):
    resp = note.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = note.delete(sample.name)
