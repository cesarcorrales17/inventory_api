from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

# Crear la aplicación FastAPI
def create_app() -> FastAPI:
    app = FastAPI(
        title="Gestión de inventario",
        description="API para gestionar el inventario de productos en un almacén.",
        version="1.0.0",
    )
 # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

 # Ruta de ejemplo
    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    return app

# Crear la instancia de la aplicación
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

