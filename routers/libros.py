from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from database import get_session
from models import Libro, Autor
from schemas import LibroCreate, LibroRead
from typing import List, Optional
router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=LibroRead, status_code=201)
def crear_libro(libro: LibroCreate, session: Session = Depends(get_session)):
    if session.exec(select(Libro).where(Libro.isbn == libro.isbn)).first():
        raise HTTPException(409, "Ya existe un libro con ese ISBN")

    nuevo_libro = Libro(
        titulo=libro.titulo,
        isbn=libro.isbn,
        anio_publicacion=libro.anio_publicacion,
        copias_disponibles=libro.copias_disponibles
    )
    if libro.autores_ids:
        autores = session.exec(select(Autor).where(Autor.id.in_(libro.autores_ids))).all()
        nuevo_libro.autores = autores
    session.add(nuevo_libro)
    session.commit()
    session.refresh(nuevo_libro)
    return nuevo_libro

@router.get("/", response_model=list[LibroRead])
def listar_libros(activo: Optional[bool] = None, session: Session = Depends(get_session)):
    query = select(Libro)
    if activo is not None:
        query = query.where(Libro.activo == activo)
    return session.exec(query).all()

