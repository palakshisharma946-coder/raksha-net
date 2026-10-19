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
    from backend.app.schemas.responses import HealthResponse
except (ImportError, ModuleNotFoundError):
    from app.core.config import settings
    from app.schemas.responses import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service Health Check",
    description="Returns operational status of the RAKSHA-NET backend service.",
    tags=["Health"],
)
async def get_health() -> HealthResponse:
    """Health check endpoint to verify backend service availability."""
    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME.lower(),
        version=settings.VERSION,
    )
