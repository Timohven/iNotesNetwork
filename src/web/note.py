import os
from fastapi import APIRouter, HTTPException
from src.model.note import Note
from src.error import Duplicate, Missing

if os.getenv("NOTE_UNIT_TEST"):
    from src.fake import note as service
    print('Fake data (web level)')
else:
    from src.service import note as service
    print('Data from DB (web level)')

router = APIRouter(prefix="/note")


@router.get("")
@router.get("/")
def get_all() -> list[Note]:
    return service.get_all()


@router.get("/{name}")
def get_specific(name) -> Note:
    try:
        return service.get_specific(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(note: Note) -> Note:
    try:
        return service.create(note)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.put("/{name}")
def modify(name: str, note: Note) -> Note:
    try:
        return service.modify(name, note)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}", status_code=204)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
