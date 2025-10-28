# 📚 Proyecto de Gestión de Biblioteca

Aplicación desarrollada con **FastAPI** y **SQLModel** para gestionar **autores, libros y sus relaciones**.  


---

## 🚀 Tecnologías utilizadas

- 🐍 **Python 3.11+**
- ⚡ **FastAPI**
- 🗃️ **SQLModel / SQLAlchemy**
- 🔥 **Uvicorn**
- 🧩 **python-dotenv** (para gestionar variables de entorno)

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