from .init import (curs, conn, IntegrityError)
from src.model.note import Note
from src.error import Missing, Duplicate

curs.execute("""create table if not exists note(
    name text primary key,
    description text,
    type_of_source text,
    source text,
    language text)""")


def row_to_model(row: tuple) -> Note:
    name, description, type_of_source, source, language = row
    return Note(name=name, description=description, type_of_source=type_of_source, source=source, language=language)


def model_to_dict(note: Note) -> dict:
    return note.model_dump()


def get_specific(name: str) -> Note:
    qry = "select * from note where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Note '{name}' not found")


def get_all() -> list[Note]:
    qry = "select * from note"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(note: Note) -> Note:
    qry = """insert into note (name, description, type_of_source, source, language)
    values (:name, :description, :type_of_source, :source, :language)"""
    params = model_to_dict(note)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(msg=f"Note '{note.name}' already exists")
    return get_specific(note.name)


def modify(name: str, note: Note) -> Note | None:
    if not (name and note):
        return None
    qry = """update note
    set name=:name,
    description=:description,
    type_of_source=:type_of_source,
    source=:source,
    language=:language
    where name=:name_orig"""
    params = model_to_dict(note)
    params["name_orig"] = name
    print(params)
    curs.execute(qry, params)
    conn.commit()
    if curs.rowcount == 1:
        print('no err')
        return get_specific(note.name)
    else:
        raise Missing(msg=f"Note '{name}' not found")


def delete(name: str):
    if not name:
        return False
    qry = "delete from note where name = :name"
    params = {"name": name}
    curs.execute(qry, params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing(msg=f"Note '{name}' not found")
