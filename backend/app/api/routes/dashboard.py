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
        DashboardAlert,
        DashboardAlertsResponse,
        DashboardOverviewResponse,
        SeverityLevel,
        SimulationState,
        utc_now,
    )
except (ImportError, ModuleNotFoundError):
    from app.schemas import (
        ApiResponse,
        DashboardAlert,
        DashboardAlertsResponse,
        DashboardOverviewResponse,
        SeverityLevel,
        SimulationState,
        utc_now,
    )

router = APIRouter()


@router.get(
    "/overview",
    response_model=ApiResponse[DashboardOverviewResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Dashboard KPI Overview (Mock)",
    description=(
        "Returns aggregated security health metrics, trust averages, and alert counts. "
        "NOTE: Returns deterministic mock data designed to power frontend dashboard summary cards."
    ),
)
async def get_dashboard_overview() -> ApiResponse[DashboardOverviewResponse]:
    """Retrieve high-level dashboard metrics in mock mode."""
    mock_overview = DashboardOverviewResponse(
        simulation_state=SimulationState.RUNNING,
        total_nodes=10,
        healthy_nodes=8,
        compromised_nodes=1,
        quarantined_nodes=1,
        average_trust_score=0.84,
        active_anomalies_count=1,
        last_updated=utc_now(),
    )

    return ApiResponse(
        status="success",
        message="Dashboard overview metrics retrieved (mock mode).",
        data=mock_overview,
    )


@router.get(
    "/alerts",
    response_model=ApiResponse[DashboardAlertsResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Security Alerts Feed (Mock)",
    description=(
        "Retrieves active and historical security alerts for the dashboard feed table. "
        "NOTE: Returns deterministic mock alert items."
    ),
)
async def get_dashboard_alerts(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum alert entries to return (1-100)",
    ),
) -> ApiResponse[DashboardAlertsResponse]:
    """Retrieve security alert feed in mock mode."""
    all_mock_alerts = [
        DashboardAlert(
            alert_id="alt-mock-001",
            node_id="node-3",
            severity=SeverityLevel.HIGH,
            title="DDoS Traffic Anomaly Detected",
            message="Outbound packet volume exceeded threshold by 380% (mock alert).",
            timestamp=utc_now(),
            is_resolved=False,
        ),
        DashboardAlert(
            alert_id="alt-mock-002",
            node_id="node-7",
            severity=SeverityLevel.MEDIUM,
            title="Elevated Packet Loss",
            message="Selective packet loss rate reached 42% on link (mock alert).",
            timestamp=utc_now(),
            is_resolved=False,
        ),
        DashboardAlert(
            alert_id="alt-mock-003",
            node_id="node-9",
            severity=SeverityLevel.LOW,
            title="Non-standard Beacon Interval",
            message="Minor beacon drift detected during routine sweep (mock alert).",
            timestamp=utc_now(),
            is_resolved=True,
        ),
    ][:limit]

    mock_alerts_response = DashboardAlertsResponse(
        total=len(all_mock_alerts),
        alerts=all_mock_alerts,
    )

    return ApiResponse(
        status="success",
        message=f"Retrieved {len(all_mock_alerts)} mock dashboard alerts.",
        data=mock_alerts_response,
    )
