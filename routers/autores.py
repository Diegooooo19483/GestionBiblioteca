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

    nuevo_autor = Autor(**autor.model_dump())  # crea desde el modelo limpio
    session.add(nuevo_autor)
    session.commit()
    session.refresh(nuevo_autor)
    return nuevo_autor


