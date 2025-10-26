from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class AutorLibro(SQLModel, table=True):
    autor_id: Optional[int] = Field(default=None, foreign_key="autor.id", primary_key=True)
    libro_id: Optional[int] = Field(default=None, foreign_key="libro.id", primary_key=True)


class Autor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais_origen: str
    anio_nacimiento: int
    activo: bool = Field(default=True)

    libros: List["Libro"] = Relationship(back_populates="autores", link_model=AutorLibro)


class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    isbn: str
    anio_publicacion: int
    copias_disponibles: int
    activo: bool = Field(default=True)

    autores: List[Autor] = Relationship(back_populates="libros", link_model=AutorLibro)
