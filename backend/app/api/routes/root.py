import sys
from pathlib import Path
from fastapi import APIRouter

# Support importing across diverse execution contexts
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from backend.app.core.config import settings
    from backend.app.schemas.responses import RootResponse
except (ImportError, ModuleNotFoundError):
    from app.core.config import settings
    from app.schemas.responses import RootResponse

router = APIRouter()


@router.get(
    "/",
    response_model=RootResponse,
    summary="Project Identification",
    description="Returns project name, status, and API info for RAKSHA-NET.",
    tags=["General"],
)
async def get_root() -> RootResponse:
    """Root endpoint identifying the application as RAKSHA-NET."""
    return RootResponse(
        project=settings.PROJECT_NAME,
        message="Welcome to RAKSHA-NET Backend API",
        version=settings.VERSION,
        status="online",
        docs_url="/docs",
    )
