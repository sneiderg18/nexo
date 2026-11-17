from fastapi import FastAPI
from routers import equipos

app = FastAPI(
    title="Nexo API",
    description="Sistema de gestión de incidentes IT - Nexo",
    version="0.1.0",
)

app.include_router(equipos.router)

@app.get("/")
def read_root():
    return {"mensaje": "Nexo API está corriendo correctamente 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}