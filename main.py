from fastapi import FastAPI
from database import init_db
from routers import autores, libros
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(autores.router)
app.include_router(libros.router)

