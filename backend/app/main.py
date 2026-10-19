import sys
from pathlib import Path

# Resolve directory paths for flexible execution from repository root or backend folder
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent
REPO_ROOT = BACKEND_DIR.parent

for path in (str(BACKEND_DIR), str(REPO_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

try:
    from backend.app.core.config import settings
    from backend.app.core.errors import (
        http_exception_handler,
        validation_exception_handler,
        generic_exception_handler,
    )
    from backend.app.api.routes import (
        root,
        health,
        simulation,
        ai,
        recovery,
        dashboard,
        network,
    )
except (ImportError, ModuleNotFoundError):
    from app.core.config import settings
    from app.core.errors import (
        http_exception_handler,
        validation_exception_handler,
        generic_exception_handler,
    )
    from app.api.routes import (
        root,
        health,
        simulation,
        ai,
        recovery,
        dashboard,
        network,
    )


def create_app() -> FastAPI:
    """Application factory for RAKSHA-NET FastAPI service."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Cross-Origin Resource Sharing (CORS) setup for future frontend / client integration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register centralized exception handlers
    application.add_exception_handler(StarletteHTTPException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    application.add_exception_handler(Exception, generic_exception_handler)

    # Register existing system endpoints
    application.include_router(root.router)
    application.include_router(health.router)

    # Register domain routers under versioned API prefix (/api/v1)
    application.include_router(
        simulation.router,
        prefix=f"{settings.API_PREFIX}/simulation",
        tags=["Simulation Engine"],
    )
    application.include_router(
        ai.router,
        prefix=f"{settings.API_PREFIX}/ai",
        tags=["AI Trust & Anomaly Engine"],
    )
    application.include_router(
        recovery.router,
        prefix=f"{settings.API_PREFIX}/recovery",
        tags=["Recovery Engine"],
    )
    application.include_router(
        dashboard.router,
        prefix=f"{settings.API_PREFIX}/dashboard",
        tags=["Dashboard"],
    )
    application.include_router(
        network.router,
        prefix=f"{settings.API_PREFIX}/network",
        tags=["Network Topology"],
    )

    return application


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
