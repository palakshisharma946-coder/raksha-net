from typing import List, Optional
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from .common import (
    NodeId,
    RecoveryActionType,
    RecoveryStatus,
    SeverityLevel,
    utc_now,
)


class RecoveryRecommendationRequest(BaseModel):
    """Request payload to query recommended mitigations for a flagged anomaly."""

    model_config = ConfigDict(extra="forbid")

    anomaly_id: str = Field(..., min_length=1, max_length=64, description="Reference anomaly identifier")
    node_id: NodeId = Field(..., description="Target node identifier")


class RecoveryRecommendationResponse(BaseModel):
    """Mitigation recommendation generated for a target node."""

    recommendation_id: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Unique recommendation identifier",
    )
    anomaly_id: str = Field(..., min_length=1, max_length=64, description="Reference anomaly identifier")
    node_id: NodeId = Field(..., description="Target node identifier")
    recommended_action: RecoveryActionType = Field(
        ...,
        description="Provisional primary recommended action",
    )
    alternative_actions: List[RecoveryActionType] = Field(
        default_factory=list,
        description="Alternative action options available",
    )
    rationale: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Decision justification for recommended action",
    )
    risk_level: SeverityLevel = Field(..., description="Risk tier associated with taking this action")
    recommended_at: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware recommendation timestamp",
    )


class RecoveryExecutionRequest(BaseModel):
    """Request payload to trigger an automated or manual recovery action."""

    model_config = ConfigDict(extra="forbid")

    node_id: NodeId = Field(..., description="Target node identifier")
    action_type: RecoveryActionType = Field(
        ...,
        description="Provisional recovery action to apply",
    )
    reason: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Audit reason for triggering action",
    )
    triggered_by: str = Field(
        default="admin",
        min_length=1,
        max_length=64,
        description="Initiator: e.g. 'autonomous_engine' or operator username",
    )
    anomaly_id: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=64,
        description="Optional associated anomaly ID",
    )


class RecoveryExecutionResponse(BaseModel):
    """Response returned upon dispatching a recovery action."""

    action_id: str = Field(..., min_length=1, max_length=64, description="Unique recovery action identifier")
    node_id: NodeId = Field(..., description="Target node identifier")
    action_type: RecoveryActionType = Field(..., description="Applied recovery action")
    status: RecoveryStatus = Field(..., description="Execution status")
    recovery_state: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Resulting node state after execution (e.g. 'quarantined', 'rerouted')",
    )
    executed_at: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware execution timestamp",
    )
    message: Optional[str] = Field(default=None, description="Optional diagnostic or outcome note")


class RecoveryActionHistory(BaseModel):
    """Audit log history of executed recovery actions."""

    total: int = Field(..., ge=0, description="Total logged recovery actions")
    actions: List[RecoveryExecutionResponse] = Field(..., description="Collection of executed recovery actions")
