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
        autores = session.exec(select(Autor).where(Autor.id.in_(libro.autores_ids))).all()#####################
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


@router.get("/anio/{anio}", response_model=list[LibroRead])
def listar_libros_anio(anio: int | None = None, session: Session = Depends(get_session)):
    query = select(Libro).where(Libro.activo == True)
    if anio:
        query = query.where(Libro.anio_publicacion == anio)
    return session.exec(query).all()


@router.get("/{libro_id}", response_model=LibroRead)
def obtener_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    return libro


@router.patch("/{libro_id}", response_model=LibroRead)
def actualizar_parcial_libro(
        libro_id: int,
        data: LibroCreate,  # Cambiado a LibroUpdate
        session: Session = Depends(get_session)
):
    libro = session.get(Libro, libro_id)

    if not libro:
        raise HTTPException(404, "Libro no encontrado")

    # Actualizar título
    if data.titulo is not None:
        libro.titulo = data.titulo

    # Actualizar ISBN (con validación)
    if data.isbn is not None:
        # Verificar que no exista otro libro con ese ISBN
        libro_existente = session.exec(
            select(Libro).where(Libro.isbn == data.isbn, Libro.id != libro_id)
        ).first()

        if libro_existente:
            raise HTTPException(409, "Ya existe un libro con ese ISBN")

        libro.isbn = data.isbn

    # Actualizar año
    if data.anio_publicacion is not None:
        libro.anio_publicacion = data.anio_publicacion

    # Actualizar copias
    if data.copias_disponibles is not None:
        libro.copias_disponibles = data.copias_disponibles

    # Actualizar autores
    if data.autores_ids is not None:
        autores = session.exec(
            select(Autor).where(Autor.id.in_(data.autores_ids))
        ).all()

        # Validar que se encontraron todos los autores
        if len(autores) != len(data.autores_ids):
            raise HTTPException(404, "Uno o más autores no encontrados")

        libro.autores = autores

    session.commit()
    session.refresh(libro)
    return libro



@router.put("/{libro_id}/activar", response_model=LibroRead)
def activar_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    libro.activo = True
    session.commit()
    session.refresh(libro)
    return libro


@router.delete("/{libro_id}", status_code=200)
def eliminar_libro(libro_id: int,eliminar_copias: bool = False,session: Session = Depends(get_session)):
    libro = session.get(Libro, libro_id)
    if not libro:
        raise HTTPException(404, "Libro no encontrado")
    libro.activo = False

    if eliminar_copias:
        libro.copias_disponibles = 0

    session.commit()

    mensaje = f"Libro '{libro.titulo}' marcado como inactivo"
    if eliminar_copias:
        mensaje += " y copias eliminadas"

    return {"mensaje": mensaje}
