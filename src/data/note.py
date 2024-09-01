from .init import (curs, conn, IntegrityError)
from src.model.note import Note
from src.error import Missing, Duplicate
import json
from pathlib import Path
from fastapi import UploadFile
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from starlette.datastructures import Headers


curs.execute("""CREATE TABLE IF NOT EXISTS Tag (
    tag_id TEXT PRIMARY KEY,
    name TEXT NOT NULL)""")

curs.execute("""CREATE TABLE IF NOT EXISTS note (
    note_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_type TEXT,
    source_link TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    files TEXT)""")

curs.execute("""CREATE TABLE IF NOT EXISTS NoteTag (
    note_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (note_id, tag_id),
    FOREIGN KEY (note_id) REFERENCES Note(note_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id) ON DELETE CASCADE)""")


# Функция для сохранения файлов и подготовки данных для базы данных
def save_files(files: Optional[List[UploadFile]], upload_dir: str) -> Optional[List[str]]:
    if files is None:
        return None
    file_paths = []
   # Создаем директорию для загрузки файлов, если она не существует
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    print('upload_path:', upload_path)
    for file in files:
        if not file.filename == '':
            unique_filename = f"{uuid4()}_{file.filename}"
            file_location = upload_path / unique_filename
            print('saving', unique_filename)
            # Сохраняем файл на диск
            with file_location.open("wb") as f:
                f.write(file.file.read())
                print('file_location:', file_location)
            file_paths.append({"filename": unique_filename,
                               "content_type": file.content_type,
                               "path": str(file_location)
                               })
    print('file_paths:', file_paths)
    return file_paths


# def download_files_to_directory(note: Note, download_dir: str):
#     # Создаем каталог, если его не существует
#     downloads_path = Path(download_dir)
#     downloads_path.mkdir(parents=True, exist_ok=True)
#
#     if note.files:
#         for upload_file in note.files:
#             # Определяем путь, куда будет сохранен файл
#             file_path = downloads_path / upload_file.filename
#
#             # Сохраняем файл в указанный путь
#             with file_path.open("wb") as buffer:
#                 buffer.write(upload_file.file.read())
#
#             print(f"File saved: {file_path}")
#     else:
#         print("No files to save.")


def row_to_model(row: tuple) -> Note:
    print('row:', row)
    note_id, title, content, source_type, source_link, created_at, updated_at, files = row
    print(type(files))
    print(files)
    # json_files = None
    # if files is not None:
    #     json_files = json.loads(files)
    files_data = json.loads(files)

    files = []
    for file_data in files_data:
        file_path = file_data["path"]
        headers = Headers({
            "content-type": file_data["content_type"],
            "content-disposition": f'form-data; name="file"; filename="{file_data["filename"]}"'
        })

        files.append(UploadFile(filename=file_data["filename"], file=open(file_path, "rb"), headers=headers))

    return Note(note_id=UUID(note_id),
                title=title,
                content=content,
                source_type=source_type,
                source_link=source_link,
                created_at=created_at,
                updated_at=updated_at,
                files=files
                )


def model_to_dict(note: Note) -> dict:
    note_dict = note.model_dump()
    note_dict['note_id'] = str(note_dict['note_id'])
    if note_dict['source_link'] is not None:
        note_dict['source_link'] = str(note_dict['source_link'])
    return note_dict


def get_specific(title: str) -> Note:
    qry = "select * from note where title=:title"
    params = {"title": title}
    curs.execute(qry, params)
    row = curs.fetchone()
    print('in get specific')
    if row:
        print(row)
        return row_to_model(row)
    else:
        raise Missing(msg=f"Note '{title}' not found")


def get_all() -> list[Note]:
    qry = "select * from note"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(note: Note) -> Note:
    qry = """insert into note (note_id, title, content, source_type, source_link, created_at, updated_at, files)
    values (:note_id, :title, :content, :source_type, :source_link, :created_at, :updated_at, :files)"""
    params = model_to_dict(note)
    print('files params in DATA', params['files'])

    # note_dict = note.model_dump()

    print('params[files][0]:', params['files'][0])
    # if (params['files'] is not None) or (params['files'][0]['filename'=='']):
    params['files'] = save_files(params['files'], "uploads")
    print(params['files'])


    # Преобразуем список файлов в JSON (или можно использовать другой способ сериализации)
    print('params after:', params['files'])
    if params['files'] is not None:
        params['files'] = json.dumps(params['files'])
    print('params after in JSON:', params['files'])
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(msg=f"Note '{note.title}' already exists")
    print(note.title)
    return note#get_specific(note.title)


def modify(title: str, note: Note) -> Note | None:
    if not (title and note):
        return None
    qry = """update note set 
    note_id=:note_id, title=:title, content=:content, source_type=:source_type, 
    source_link=:source_link, created_at=:created_at, updated_at=:updated_at, files=:files
    where title=:title_orig"""
    params = model_to_dict(note)
    if params['files'] is not None:
        params['files'] = json.dumps(params['files'])
    params["title_orig"] = title
    print(params)
    print('run')
    curs.execute(qry, params)
    conn.commit()
    if curs.rowcount == 1:
        print('no err')
        return get_specific(note.title)
    else:
        raise Missing(msg=f"Note '{title}' not found")


def delete(title: str):
    if not title:
        return False
    qry = "delete from note where title = :title"
    params = {"title": title}
    curs.execute(qry, params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing(msg=f"Note '{title}' not found")
