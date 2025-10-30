# 📚 Proyecto de Gestión de Biblioteca

Aplicación desarrollada con **FastAPI** y **SQLModel** para gestionar **autores, libros y sus relaciones**.  


---

## 🚀 Tecnologías utilizadas

- 🐍 **Python 3.11+**
- ⚡ **FastAPI**
- 🗃️ **SQLModel / SQLAlchemy**
- 🔥 **Uvicorn**

---

## ⚙️ Instalación y configuración

### 1️. Clona el repositorio
```bash
git clone https://github.com/tu-usuario/GestionBibliotecaParcial.git
cd GestionBibliotecaParcial

```
### 2. Crea y activa un entorno virtual
```bash
python -m venv venv 
venv\Scripts\activate #Windows

python -m venv venv 
source venv\Scripts\activate #Linux
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt


Si no esta el archivo requirements.txt, generalo con:
pip freeze > requirements.txt
```

## 🖥️ Ejecucion de servidor 

```bash

uvicorn main:app --reload

```

## 📊 Poblar datos

```bash

python seed.py
```
## 🗒️ Clases
| Clase           | Atributos                                                                             |
| --------------- | ------------------------------------------------------------------------------------- |
| **Autor**       | `id`, `nombre`, `pais`, `anio_nacimiento`, `activo`, `libros`                         |
| **Libro**       | `id`, `titulo`, `isbn`, `anio_publicacion`, `copias_disponibles`, `activo`, `autores` |
| **AutorLibro**  | `autor_id`, `libro_id`                                                                |


## 🗺️ Mapa de endpoints

### 🎓 AUTORES
| Método   | Endpoint              | Descripción                                                                               |
| -------- | --------------------- | ----------------------------------------------------------------------------------------- |
| `GET`    | `/autores/`           | Lista todos los autores (activos o inactivos, según el parámetro `activos`).              |
| `GET`    | `/autores/{autor_id}` | Obtiene la información de un autor específico.                                            |
| `POST`   | `/autores/`           | Crea un nuevo autor (recibe nombre, país, año nacimiento).                                |
| `PUT`    | `/autores/{autor_id}` | Actualiza los datos de un autor existente. Si un campo no se envía, conserva el anterior. |
| `DELETE` | `/autores/{autor_id}` | Desactiva al autor (no elimina). Si el autor es único de un libro, desactiva ese libro.   |
| `GET`    | `/autores/filtrar/`   | Filtra autores por país.                                                                  |

### 📒 LIBROS

| Método   | Endpoint                             | Descripción                                                 |
| -------- | ------------------------------------ | ----------------------------------------------------------- |
| `GET`    | `/libros/`                           | Lista todos los libros existentes.                          |
| `GET`    | `/libros/{libro_id}`                 | Obtiene un libro específico por ID.                         |
| `POST`   | `/libros/`                           | Crea un nuevo libro con autores asociados.                  |
| `PUT`    | `/libros/{libro_id}`                 | Actualiza un libro (mantiene valores previos si se omiten). |
| `DELETE` | `/libros/{libro_id}`                 | Desactiva un libro sin eliminarlo.                          |
| `GET`    | `/libros/por_autor/{autor_id}`       | Lista todos los libros de un autor específico.              |
| `GET`    | `/libros/autores/{libro_id}`         | Muestra los autores asociados a un libro.                   |
| `GET`    | `/libros/por_anio/{anio}`            | Lista todos los libros publicados en un año determinado.    |
| `POST`   | `/libros/{libro_id}/copias/eliminar` | Elimina una copia de un libro y actualiza el conteo.        |

### 📎 RELACIONES
| Modelo                   | Atributos principales                                                      | Relaciones                                                         |
| ------------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Autor**                | `id`, `nombre`, `pais`, `anio_nacimiento`, `activo`                        | Relación N:M  **muchos a muchos** con `Libro`                      |
| **Libro**                | `id`, `titulo`, `isbn`, `anio_publicacion`, `copias_disponibles`, `activo` | Relación N:M  **muchos a muchos** con `Autor`                     |
| **Relación Autor-Libro** | Tabla intermedia (many-to-many)                                            | Relación N:M                                                       |
