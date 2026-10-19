from typing import List, Optional
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from .common import (
    NodeId,
    SeverityLevel,
    TrustLevel,
    utc_now,
)


class TrustEvaluationRequest(BaseModel):
    """Request payload to compute or refresh trust scores for given nodes."""

    model_config = ConfigDict(extra="forbid")

    node_ids: List[NodeId] = Field(
        ...,
        min_length=1,
        description="List of node identifiers to evaluate",
    )


class NodeTrustScore(BaseModel):
    """Trust score and confidence rating for an individual node."""

    node_id: NodeId = Field(..., description="Node identifier")
    trust_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Computed trust score in range 0.0 (untrusted) to 1.0 (fully trusted)",
    )
    trust_level: TrustLevel = Field(..., description="Categorical trust classification")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="AI model confidence score in range 0.0 to 1.0",
    )
    evaluated_at: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware evaluation timestamp",
    )


class TrustEvaluationResponse(BaseModel):
    """Response containing evaluated trust scores across queried nodes."""

    evaluated_at: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware batch evaluation timestamp",
    )
    scores: List[NodeTrustScore] = Field(..., description="List of per-node trust ratings")


class AnomalyDetectionRequest(BaseModel):
    """Request parameters to trigger or filter anomaly detection."""

    model_config = ConfigDict(extra="forbid")

    simulation_id: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=64,
        description="Optional simulation run filter",
    )
    node_ids: Optional[List[NodeId]] = Field(
        default=None,
        description="Optional target node filters",
    )
    time_window_seconds: int = Field(
        default=60,
        ge=1,
        le=3600,
        description="Analysis time window in seconds (1 to 3600)",
    )


class AnomalyRecord(BaseModel):
    """Detected anomaly event details."""

    anomaly_id: str = Field(..., min_length=1, max_length=64, description="Unique anomaly record identifier")
    node_id: NodeId = Field(..., description="Target node identifier")
    anomaly_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Category or pattern label of detected anomaly",
    )
    severity: SeverityLevel = Field(..., description="Threat severity tier")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="AI detection confidence rating in range 0.0 to 1.0",
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Human-readable explanation of detected abnormal behavior",
    )
    detected_at: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware detection timestamp",
    )


class AnomalyListResponse(BaseModel):
    """List of detected anomalies returned to callers."""

    total: int = Field(..., ge=0, description="Total count of anomalies matching criteria")
    anomalies: List[AnomalyRecord] = Field(..., description="Collection of anomaly records")
