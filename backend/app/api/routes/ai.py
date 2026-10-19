import sys
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Query, status

# Support importing across diverse execution contexts
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from backend.app.schemas import (
        AnomalyDetectionRequest,
        AnomalyListResponse,
        AnomalyRecord,
        ApiResponse,
        NodeTrustScore,
        SeverityLevel,
        TrustEvaluationRequest,
        TrustEvaluationResponse,
        TrustLevel,
        utc_now,
    )
except (ImportError, ModuleNotFoundError):
    from app.schemas import (
        AnomalyDetectionRequest,
        AnomalyListResponse,
        AnomalyRecord,
        ApiResponse,
        NodeTrustScore,
        SeverityLevel,
        TrustEvaluationRequest,
        TrustEvaluationResponse,
        TrustLevel,
        utc_now,
    )

router = APIRouter()


@router.post(
    "/evaluate-trust",
    response_model=ApiResponse[TrustEvaluationResponse],
    status_code=status.HTTP_200_OK,
    summary="Evaluate Node Trust Scores (Mock)",
    description=(
        "Evaluates Zero-Trust scores for requested nodes based on behavioral telemetry. "
        "NOTE: Currently operates as a mock shell returning deterministic trust ratings; "
        "no real ML model inference is executed."
    ),
)
async def evaluate_trust(payload: TrustEvaluationRequest) -> ApiResponse[TrustEvaluationResponse]:
    """Evaluate trust scores for given nodes with deterministic mock data."""
    scores: List[NodeTrustScore] = []

    for node_id in payload.node_ids:
        # Deterministic mock assignment: flagged nodes get lower score
        if "bad" in node_id.lower() or "compromised" in node_id.lower() or "3" in node_id:
            score = 0.32
            level = TrustLevel.UNTRUSTED
            confidence = 0.91
        else:
            score = 0.94
            level = TrustLevel.TRUSTED
            confidence = 0.96

        scores.append(
            NodeTrustScore(
                node_id=node_id,
                trust_score=score,
                trust_level=level,
                confidence=confidence,
                evaluated_at=utc_now(),
            )
        )

    mock_response = TrustEvaluationResponse(
        evaluated_at=utc_now(),
        scores=scores,
    )

    return ApiResponse(
        status="success",
        message="Trust evaluation completed in mock mode (synthetic ratings returned).",
        data=mock_response,
    )


@router.get(
    "/anomalies",
    response_model=ApiResponse[AnomalyListResponse],
    status_code=status.HTTP_200_OK,
    summary="List Detected Anomalies (Mock)",
    description=(
        "Retrieves detected security anomalies and threat alerts. "
        "NOTE: Returns deterministic mock anomaly records."
    ),
)
async def list_anomalies(
    severity: Optional[SeverityLevel] = Query(
        default=None,
        description="Filter anomalies by threat severity tier",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of anomaly records to return (1-100)",
    ),
) -> ApiResponse[AnomalyListResponse]:
    """Retrieve filtered list of mock anomalies."""
    all_mock_anomalies = [
        AnomalyRecord(
            anomaly_id="anom-mock-001",
            node_id="node-3",
            anomaly_type="traffic_spike_ddos",
            severity=SeverityLevel.HIGH,
            confidence=0.94,
            description="Outbound packet rate exceeded expected baseline by 380% (mock detection).",
            detected_at=utc_now(),
        ),
        AnomalyRecord(
            anomaly_id="anom-mock-002",
            node_id="node-7",
            anomaly_type="packet_drop_tampering",
            severity=SeverityLevel.MEDIUM,
            confidence=0.88,
            description="Selective forwarding drop rate reached 42% (mock detection).",
            detected_at=utc_now(),
        ),
        AnomalyRecord(
            anomaly_id="anom-mock-003",
            node_id="node-9",
            anomaly_type="unauthorized_beacon",
            severity=SeverityLevel.LOW,
            confidence=0.75,
            description="Non-standard broadcast interval detected (mock detection).",
            detected_at=utc_now(),
        ),
    ]

    filtered = [
        a for a in all_mock_anomalies
        if severity is None or a.severity == severity
    ][:limit]

    mock_result = AnomalyListResponse(
        total=len(filtered),
        anomalies=filtered,
    )

    return ApiResponse(
        status="success",
        message=f"Retrieved {len(filtered)} mock anomaly records.",
        data=mock_result,
    )


@router.post(
    "/detect-anomalies",
    response_model=ApiResponse[AnomalyListResponse],
    status_code=status.HTTP_200_OK,
    summary="Trigger Anomaly Detection (Mock)",
    description=(
        "Triggers on-demand anomaly inspection on target nodes or simulation window. "
        "NOTE: Mock shell returns synthetic detection results."
    ),
)
async def detect_anomalies(payload: AnomalyDetectionRequest) -> ApiResponse[AnomalyListResponse]:
    """Trigger on-demand mock anomaly detection."""
    target_nodes = payload.node_ids or ["node-3"]
    anomalies: List[AnomalyRecord] = []

    for idx, nid in enumerate(target_nodes, start=1):
        anomalies.append(
            AnomalyRecord(
                anomaly_id=f"anom-mock-live-{idx:03d}",
                node_id=nid,
                anomaly_type="behavioral_deviation",
                severity=SeverityLevel.MEDIUM,
                confidence=0.89,
                description=f"Behavioral drift observed in time window {payload.time_window_seconds}s (mock result).",
                detected_at=utc_now(),
            )
        )

    mock_result = AnomalyListResponse(
        total=len(anomalies),
        anomalies=anomalies,
    )

    return ApiResponse(
        status="success",
        message="On-demand anomaly inspection completed in mock mode.",
        data=mock_result,
    )
