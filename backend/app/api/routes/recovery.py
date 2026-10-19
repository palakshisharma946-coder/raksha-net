import sys
from pathlib import Path
from fastapi import APIRouter, Query, status

# Support importing across diverse execution contexts
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from backend.app.schemas import (
        ApiResponse,
        RecoveryActionHistory,
        RecoveryActionType,
        RecoveryExecutionRequest,
        RecoveryExecutionResponse,
        RecoveryRecommendationRequest,
        RecoveryRecommendationResponse,
        RecoveryStatus,
        SeverityLevel,
        utc_now,
    )
except (ImportError, ModuleNotFoundError):
    from app.schemas import (
        ApiResponse,
        RecoveryActionHistory,
        RecoveryActionType,
        RecoveryExecutionRequest,
        RecoveryExecutionResponse,
        RecoveryRecommendationRequest,
        RecoveryRecommendationResponse,
        RecoveryStatus,
        SeverityLevel,
        utc_now,
    )

router = APIRouter()


@router.post(
    "/recommend",
    response_model=ApiResponse[RecoveryRecommendationResponse],
    status_code=status.HTTP_200_OK,
    summary="Generate Mitigation Recommendation (Mock)",
    description=(
        "Analyzes anomaly details and recommends suitable self-healing or mitigation action. "
        "NOTE: Currently operates as a mock shell returning a deterministic policy recommendation."
    ),
)
async def recommend_recovery(
    payload: RecoveryRecommendationRequest,
) -> ApiResponse[RecoveryRecommendationResponse]:
    """Provide mitigation recommendation for a target anomaly."""
    mock_rec = RecoveryRecommendationResponse(
        recommendation_id=f"rec-mock-{payload.node_id}-001",
        anomaly_id=payload.anomaly_id,
        node_id=payload.node_id,
        recommended_action=RecoveryActionType.QUARANTINE_NODE,
        alternative_actions=[
            RecoveryActionType.RATE_LIMIT,
            RecoveryActionType.REROUTE_TRAFFIC,
        ],
        rationale=(
            f"Automated policy: severe traffic anomaly on node '{payload.node_id}' "
            "requires isolation to protect mesh routing integrity (mock rationale)."
        ),
        risk_level=SeverityLevel.HIGH,
        recommended_at=utc_now(),
    )

    return ApiResponse(
        status="success",
        message="Mitigation recommendation generated in mock mode.",
        data=mock_rec,
    )


@router.post(
    "/execute",
    response_model=ApiResponse[RecoveryExecutionResponse],
    status_code=status.HTTP_200_OK,
    summary="Execute Recovery Action (Mock)",
    description=(
        "Applies a remediation action (e.g. quarantine, rate limit, reroute) to target node. "
        "NOTE: Confined to mock response; does NOT modify physical network or external host systems."
    ),
)
async def execute_recovery(
    payload: RecoveryExecutionRequest,
) -> ApiResponse[RecoveryExecutionResponse]:
    """Simulate execution of a recovery mitigation action."""
    mock_action = RecoveryExecutionResponse(
        action_id=f"act-mock-{payload.action_type.value}-001",
        node_id=payload.node_id,
        action_type=payload.action_type,
        status=RecoveryStatus.COMPLETED,
        recovery_state=f"applied_{payload.action_type.value}_mock",
        executed_at=utc_now(),
        message=(
            f"Remediation action '{payload.action_type.value}' recorded for '{payload.node_id}' "
            "(mock mode: no real network actuators invoked)."
        ),
    )

    return ApiResponse(
        status="success",
        message="Recovery action executed in mock mode.",
        data=mock_action,
    )


@router.get(
    "/actions",
    response_model=ApiResponse[RecoveryActionHistory],
    status_code=status.HTTP_200_OK,
    summary="Get Recovery Action Audit History (Mock)",
    description=(
        "Retrieves historical audit log of remediation actions applied across the network. "
        "NOTE: Returns deterministic mock log records."
    ),
)
async def get_recovery_actions(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum action log entries to return (1-100)",
    ),
) -> ApiResponse[RecoveryActionHistory]:
    """Retrieve mock recovery action history."""
    all_mock_actions = [
        RecoveryExecutionResponse(
            action_id="act-mock-hist-001",
            node_id="node-3",
            action_type=RecoveryActionType.QUARANTINE_NODE,
            status=RecoveryStatus.COMPLETED,
            recovery_state="node_isolated",
            executed_at=utc_now(),
            message="Node quarantined due to DDoS anomaly (mock audit record).",
        ),
        RecoveryExecutionResponse(
            action_id="act-mock-hist-002",
            node_id="node-7",
            action_type=RecoveryActionType.REROUTE_TRAFFIC,
            status=RecoveryStatus.COMPLETED,
            recovery_state="traffic_diverted",
            executed_at=utc_now(),
            message="Traffic rerouted to alternate hop (mock audit record).",
        ),
    ][:limit]

    mock_history = RecoveryActionHistory(
        total=len(all_mock_actions),
        actions=all_mock_actions,
    )

    return ApiResponse(
        status="success",
        message=f"Retrieved {len(all_mock_actions)} mock recovery action log records.",
        data=mock_history,
    )
