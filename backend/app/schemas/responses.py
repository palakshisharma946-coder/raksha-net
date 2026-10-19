from typing import Any, Optional
from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Schema for root identification endpoint."""

    project: str = Field(..., description="Project name")
    message: str = Field(..., description="Welcome or status message")
    version: str = Field(..., description="API version")
    status: str = Field(..., description="Application operational status")
    docs_url: str = Field(..., description="Interactive API documentation URL")


class HealthResponse(BaseModel):
    """Schema for service health check endpoint."""

    status: str = Field(..., description="Service health state")
    service: str = Field(..., description="Name of the service")
    version: str = Field(..., description="Service version")


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    status: str = Field(default="error", description="Error indicator")
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Human-readable error description")
    details: Optional[Any] = Field(default=None, description="Detailed error breakdown if available")
