from fastapi import FastAPI
from database import init_db
from routers import autores, libros

app = FastAPI(title="Gestión de Biblioteca")

app.include_router(autores.router)
app.include_router(libros.router)

@app.on_event("startup")
def startup_event():
    init_db()
