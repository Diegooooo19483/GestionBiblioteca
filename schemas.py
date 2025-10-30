from typing import List, Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

# Autor ---------------------------------------------------------
class AutorBase(SQLModel):
    nombre: str = Field(min_length=2,max_length=100,description="Nombre completo del autor")
    pais_origen: str = Field(min_length=2,max_length=50,description="País de origen del autor")
    anio_nacimiento: int = Field(ge=1000,description="Año de nacimiento del autor")

class AutorCreate(AutorBase):
    pass

class AutorRead(AutorBase):
    id: int
    activo: bool
    class Config:
        orm_mode = True

# Libro --------------------------------------------
class LibroBase(SQLModel):
    titulo: str = Field(min_length=1,max_length=200,description="Título del libro")
    isbn: str = Field(min_length=6,max_length=20,description="Código ISBN del libro")
    anio_publicacion: int = Field(ge=1000,le=datetime.now().year,description="Año de publicación del libro")
    copias_disponibles: int = Field(ge=0,le=1000,description="Cantidad de copias disponibles en biblioteca")


class LibroCreate(SQLModel):
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(default=None, min_length=6, max_length=13)
    anio_publicacion: Optional[int] = Field(default=None, ge=1000)
    copias_disponibles: Optional[int] = Field(default=None, ge=0, le=1000)
    autores_ids: Optional[List[int]] = None



class LibroRead(LibroBase):
    id: int
    activo: bool
    autores: List[AutorRead] = []
    class Config:
        orm_mode = True

class AutorReadConLibros(AutorRead):
    libros: List[LibroRead] = []
