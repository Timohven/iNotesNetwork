from pathlib import Path

UPLOAD_DIRECTORY = "uploads"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)
# DOWNLOAD_DIRECTORY = "downloads"
# Path(DOWNLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)


import os
from fastapi import APIRouter, HTTPException, Request, Depends, Form, UploadFile, File, Path, status
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import HttpUrl, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Optional
from src.model.note import Note
from src.error import Duplicate, Missing
from fastapi.templating import Jinja2Templates
from uuid import uuid4
import shutil


# os.environ["NOTE_UNIT_TEST"] = 'True'
if os.getenv("NOTE_UNIT_TEST"):
    from src.fake import note as service
    print('Fake data (web level)')
else:
    from src.service import note as service
    print('Data from DB (web level)')

template = Jinja2Templates(directory="templates/")

router = APIRouter(prefix="/note")


@router.post("/all")
# def add_note_in_template(request: Request, note: Note = Depends(Note.as_form)):
# unable to read parametr "note"
def add_note_in_template(request: Request,
                         title: str = Form(...),
                         content: str = Form(...),
                         source_type: str = Form(...),
                         source_link: Optional[HttpUrl] = Form(...),
                         files: List[UploadFile] = File([])
                         ):
    # print('len of files:', len(files))
    # print('type of files:', type(files[0]), 'files content:', files)
    note = Note(title=title,
                content=content,
                source_type=source_type,
                source_link=source_link,
                files=files)
    # print('Note created in WEB:', note)
    try:
        service.create(note)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    # print('after create')
    note_list = service.get_all()
    # print('after get_all')
    return template.TemplateResponse("notes.html", {
        "request": request,
        "notes": note_list
    })


@router.get("/all")
def get_all_in_template(request: Request):
    note_list = service.get_all()
    return template.TemplateResponse("notes.html", {
        "request": request,
        "notes": note_list
    })


# @router.get("/download/{filename}")
# async def download_file(filename: str):
#     file_path = os.path.join("uploads", filename)
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
#     return FileResponse(file_path, media_type='application/octet-stream', filename=filename)


@router.get("/downloads/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("uploads", filename)
    print('filename:', filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # downloads_path = Path('downloads')
    # downloads_path.mkdir(parents=True, exist_ok=True)
    downloads_path = os.path.join('downloads', filename)
    with open(downloads_path, "wb") as f:
        shutil.copyfileobj(open(file_path, 'rb'), f)

    return RedirectResponse(url=f"/static/{filename}")


@router.get("/{title}")
def get_specific_in_template(request: Request, title: str = Path(..., title="The Name of the note to retrieve.")):
    note_list = service.get_all()
    for note in note_list:
        if note.title == title:
            return template.TemplateResponse(
                "notes.html", {
                    "request": request,
                    "note": note
                })
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note with supplied name doesn't exist",
    )


@router.get("/{title}")
def get_specific(title) -> Note:
    try:
        return service.get_specific(title)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.get("")
@router.get("/")
def get_all() -> list[Note]:
    return service.get_all()


@router.post("/", status_code=201)
def create(note: Note) -> Note:
    try:
        return service.create(note)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.put("/{title}")
def modify(title: str, note: Note) -> Note:
    try:
        return service.modify(title, note)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{title}", status_code=204)
def delete(title: str):
    try:
        return service.delete(title)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# @router.post("/upload/")
# async def upload_big_file(files: List[UploadFile] = File(...)) -> str:
#     for file in files:
#         unique_filename = f"{uuid4()}_{file.filename}"
#         file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
#         with open(file_location, "wb") as f:
#             f.write(await file.read())
#     return f"file size: {file.size}, name: {file.filename}"