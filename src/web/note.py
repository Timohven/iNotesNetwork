import os
from fastapi import APIRouter, HTTPException, Request, Depends, Path, status
from src.model.note import Note
from src.error import Duplicate, Missing
from fastapi.templating import Jinja2Templates

if os.getenv("NOTE_UNIT_TEST"):
    from src.fake import note as service
    print('Fake data (web level)')
else:
    from src.service import note as service
    print('Data from DB (web level)')

template = Jinja2Templates(directory="templates/")

router = APIRouter(prefix="/note")


@router.post("/all")
def add_note(request: Request, note: Note = Depends(Note.as_form)):
    try:
        service.create(note)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    note_list = service.get_all()
    return template.TemplateResponse("notes.html", {
        "request": request,
        "notes": note_list
    })


@router.get("/all")
def get_notes(request: Request):
    note_list = service.get_all()
    return template.TemplateResponse("notes.html", {
        "request": request,
        "notes": note_list
    })


@router.get("/{note_name}")
def get_single_note(request: Request, note_name: str = Path(..., title="The Name of the note to retrieve.")):
    note_list = service.get_all()
    for note in note_list:
        if note.name == note_name:
            return template.TemplateResponse(
                "notes.html", {
                    "request": request,
                    "note": note
                })
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note with supplied name doesn't exist",
    )


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
