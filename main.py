from fastapi import FastAPI
from database import init_db
from routers import autores, libros
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)
app.include_router(autores.router)
app.include_router(libros.router)

@app.on_event("startup")
def startup_event():
    init_db()
