"""Pydantic models and schemas for request/response serialization."""

from .ai import (
    AnomalyDetectionRequest,
    AnomalyListResponse,
    AnomalyRecord,
    NodeTrustScore,
    TrustEvaluationRequest,
    TrustEvaluationResponse,
)
from .common import (
    ApiResponse,
    AttackIntensity,
    AttackType,
    NodeId,
    NodeStatus,
    RecoveryActionType,
    RecoveryStatus,
    SeverityLevel,
    SimulationState,
    TopologyType,
    TrustLevel,
    utc_now,
)
from .dashboard import (
    DashboardAlert,
    DashboardAlertsResponse,
    DashboardOverviewResponse,
    NetworkLink,
    NetworkNode,
    NetworkTopologyResponse,
    NodeDetailResponse,
)
from .recovery import (
    RecoveryActionHistory,
    RecoveryExecutionRequest,
    RecoveryExecutionResponse,
    RecoveryRecommendationRequest,
    RecoveryRecommendationResponse,
)
from .responses import (
    ErrorResponse,
    HealthResponse,
    RootResponse,
)
from .simulation import (
    AttackInjectionRequest,
    AttackInjectionResponse,
    SimulationStartRequest,
    SimulationStateResponse,
    SimulationStopRequest,
    SimulationStopResponse,
    TelemetryBatchRequest,
    TelemetryIngestResponse,
    TelemetryRecord,
)

__all__ = [
    # Common
    "ApiResponse",
    "NodeId",
    "NodeStatus",
    "SeverityLevel",
    "TrustLevel",
    "SimulationState",
    "TopologyType",
    "AttackType",
    "AttackIntensity",
    "RecoveryActionType",
    "RecoveryStatus",
    "utc_now",
    # Legacy / Health
    "RootResponse",
    "HealthResponse",
    "ErrorResponse",
    # Simulation
    "SimulationStartRequest",
    "SimulationStateResponse",
    "SimulationStopRequest",
    "SimulationStopResponse",
    "AttackInjectionRequest",
    "AttackInjectionResponse",
    "TelemetryRecord",
    "TelemetryBatchRequest",
    "TelemetryIngestResponse",
    # AI
    "TrustEvaluationRequest",
    "NodeTrustScore",
    "TrustEvaluationResponse",
    "AnomalyDetectionRequest",
    "AnomalyRecord",
    "AnomalyListResponse",
    # Recovery
    "RecoveryRecommendationRequest",
    "RecoveryRecommendationResponse",
    "RecoveryExecutionRequest",
    "RecoveryExecutionResponse",
    "RecoveryActionHistory",
    # Dashboard
    "DashboardOverviewResponse",
    "NetworkNode",
    "NetworkLink",
    "NetworkTopologyResponse",
    "NodeDetailResponse",
    "DashboardAlert",
    "DashboardAlertsResponse",
]
