from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Autor, Libro, AutorLibro
from schemas import AutorRead, AutorCreate
from database import get_session
from typing import List, Optional
router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", response_model=AutorRead, status_code=201)
def crear_autor(autor: AutorCreate, session: Session = Depends(get_session)):
    existe = session.exec(select(Autor).where(Autor.nombre == autor.nombre)).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un autor con ese nombre")

    nuevo_autor = Autor(**autor.model_dump())###############v
    session.add(nuevo_autor)
    session.commit()
    session.refresh(nuevo_autor)
    return nuevo_autor

@router.get("/", response_model=list[AutorRead])
def listar_autores(activo: Optional[bool] = None, session: Session = Depends(get_session)):
    query = select(Autor)
    if activo is not None:
        query = query.where(Autor.activo == activo)
    return session.exec(query).all()##################



@router.get("/pais/{pais}")
def filtrar_autores_por_pais(pais: str, session: Session = Depends(get_session)):
    autores = session.exec(select(Autor).where(Autor.pais_origen == pais)).all()##############all
    return autores


@router.get("/{autor_id}/libros")
def libros_por_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor, autor.libros


@router.put("/{autor_id}", response_model=AutorRead)
def actualizar_autor(autor_id: int, data: AutorCreate, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)

    if not autor:
        raise HTTPException(status_code=404, detail="autor no encontrado")

    if data.nombre is not None:
        autor.nombre = data.nombre
    if data.pais_origen is not None:
        autor.pais_origen = data.pais_origen
    if data.anio_nacimiento is not None:
        autor.anio_nacimiento = data.anio_nacimiento
    session.commit()
    session.refresh(autor)
    return autor

@router.delete("/desactivar/{autor_id}")
def desactivar_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    autor.activo = False
    for libro in autor.libros:

        if len(libro.autores) == 1:
            libro.activo = False
    session.commit()
    return {"mensaje": f"Autor {autor.nombre} desactivado y libros únicos desactivados."}

@router.put("/{autor_id}/activar", response_model=AutorRead)
def activar_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(404, "Autor no encontrado")

    autor.activo = True
    for libro in autor.libros:
        # si el libro solo tiene ese autor
        if len(libro.autores) == 1:
            libro.activo = True

    session.commit()
    session.refresh(autor)
    return autor
