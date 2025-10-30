from sqlmodel import Session
from database import engine
from models import Autor, Libro, AutorLibro

def poblar_datos():
    with Session(engine) as session:
        autor1 = Autor(nombre="Gabriel García Márquez", pais_origen="Colombia", anio_nacimiento=1927)
        autor2 = Autor(nombre="Isabel Allende", pais_origen="Chile", anio_nacimiento=1942)

        libro1 = Libro(titulo="Cien años de soledad", isbn="123456", anio_publicacion=1967, copias_disponibles=5)
        libro2 = Libro(titulo="La casa de los espíritus", isbn="789012", anio_publicacion=1982, copias_disponibles=3)

        session.add_all([autor1, autor2, libro1, libro2])
        session.commit()

        session.add_all([
            AutorLibro(autor_id=autor1.id, libro_id=libro1.id),
            AutorLibro(autor_id=autor2.id, libro_id=libro2.id)
        ])
        session.commit()
        print("📚 Datos insertados correctamente.")

if __name__ == "__main__":
    poblar_datos()
