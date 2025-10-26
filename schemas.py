from typing import List, Optional
from sqlmodel import SQLModel

# ======== Autor =========
class AutorBase(SQLModel):
    nombre: str
    pais_origen: str
    anio_nacimiento: int

class AutorCreate(SQLModel):
    nombre: Optional[str] = None
    pais_origen: Optional[str] = None
    anio_nacimiento: Optional[int] = None

class AutorRead(AutorBase):
    id: int
    activo: bool
    class Config:
        orm_mode = True

# ======== Libro =========
class LibroBase(SQLModel):
    titulo: str
    isbn: str
    anio_publicacion: int
    copias_disponibles: int


class LibroCreate(SQLModel):
    titulo: Optional[str] = None
    isbn: Optional[str] = None
    anio_publicacion: Optional[int] = None
    copias_disponibles: Optional[int] = None
    autores_ids: Optional[List[int]] = None



class LibroRead(LibroBase):
    id: int
    activo: bool
    autores: List[AutorRead] = []
    class Config:
        orm_mode = True

class AutorReadConLibros(AutorRead):
    libros: List[LibroRead] = []
