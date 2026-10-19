import sys
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Query, status

# Support importing across diverse execution contexts
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from backend.app.schemas import (
        ApiResponse,
        AttackInjectionRequest,
        AttackInjectionResponse,
        SimulationStartRequest,
        SimulationState,
        SimulationStateResponse,
        SimulationStopRequest,
        SimulationStopResponse,
        TelemetryBatchRequest,
        TelemetryIngestResponse,
        TopologyType,
        utc_now,
    )
except (ImportError, ModuleNotFoundError):
    from app.schemas import (
        ApiResponse,
        AttackInjectionRequest,
        AttackInjectionResponse,
        SimulationStartRequest,
        SimulationState,
        SimulationStateResponse,
        SimulationStopRequest,
        SimulationStopResponse,
        TelemetryBatchRequest,
        TelemetryIngestResponse,
        TopologyType,
        utc_now,
    )

router = APIRouter()


@router.post(
    "/start",
    response_model=ApiResponse[SimulationStateResponse],
    status_code=status.HTTP_200_OK,
    summary="Start Simulation Run (Mock)",
    description=(
        "Initiates a virtual network simulation run with specified topology and traffic parameters. "
        "NOTE: Currently operates as a mock shell; no actual virtual network or sockets are initialized."
    ),
)
async def start_simulation(payload: SimulationStartRequest) -> ApiResponse[SimulationStateResponse]:
    """Start simulation endpoint returning deterministic mock execution state."""
    # Deterministic mock simulation identifier
    mock_sim_id = f"sim-mock-{payload.topology_type.value}-{payload.node_count}"

    mock_state = SimulationStateResponse(
        simulation_id=mock_sim_id,
        state=SimulationState.RUNNING,
        topology_type=payload.topology_type,
        active_nodes=payload.node_count,
        started_at=utc_now(),
        elapsed_seconds=0,
    )

    return ApiResponse(
        status="success",
        message="Simulation run initialized in mock mode (no physical/virtual network started).",
        data=mock_state,
    )


@router.post(
    "/stop",
    response_model=ApiResponse[SimulationStopResponse],
    status_code=status.HTTP_200_OK,
    summary="Stop Simulation Run (Mock)",
    description=(
        "Halts an active network simulation run. "
        "NOTE: Currently operates as a mock shell returning confirmation of stoppage."
    ),
)
async def stop_simulation(payload: SimulationStopRequest) -> ApiResponse[SimulationStopResponse]:
    """Stop simulation endpoint returning deterministic mock stop response."""
    mock_stop = SimulationStopResponse(
        simulation_id=payload.simulation_id,
        state=SimulationState.STOPPED,
        stopped_at=utc_now(),
        total_runtime_seconds=120,
    )

    return ApiResponse(
        status="success",
        message=f"Simulation '{payload.simulation_id}' halted in mock mode.",
        data=mock_stop,
    )


@router.get(
    "/status",
    response_model=ApiResponse[SimulationStateResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Simulation Status (Mock)",
    description=(
        "Queries current execution lifecycle and active metrics of network simulation. "
        "NOTE: Returns deterministic mock telemetry status."
    ),
)
async def get_simulation_status(
    simulation_id: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=64,
        description="Optional simulation run identifier to query",
    ),
) -> ApiResponse[SimulationStateResponse]:
    """Retrieve operational state for target simulation."""
    active_id = simulation_id or "sim-mock-default"

    mock_status = SimulationStateResponse(
        simulation_id=active_id,
        state=SimulationState.RUNNING,
        topology_type=TopologyType.MESH,
        active_nodes=10,
        started_at=utc_now(),
        elapsed_seconds=45,
    )

    return ApiResponse(
        status="success",
        message=f"Simulation status for '{active_id}' retrieved (mock mode).",
        data=mock_status,
    )


@router.post(
    "/attack",
    response_model=ApiResponse[AttackInjectionResponse],
    status_code=status.HTTP_200_OK,
    summary="Inject Simulated Attack (Mock)",
    description=(
        "Simulates a cyber attack (e.g. DDoS, Sybil, Blackhole) targeting designated nodes. "
        "NOTE: Mock shell only; does NOT launch any real network attack or packet flood."
    ),
)
async def inject_attack(payload: AttackInjectionRequest) -> ApiResponse[AttackInjectionResponse]:
    """Record simulated attack injection."""
    mock_attack_id = f"atk-mock-{payload.attack_type.value}-001"

    mock_response = AttackInjectionResponse(
        attack_id=mock_attack_id,
        attack_type=payload.attack_type,
        target_node_ids=payload.target_node_ids,
        status="injected_mock",
        injected_at=utc_now(),
    )

    return ApiResponse(
        status="success",
        message="Simulated attack recorded in mock mode (no live network traffic generated).",
        data=mock_response,
    )


@router.post(
    "/telemetry",
    response_model=ApiResponse[TelemetryIngestResponse],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest Telemetry Batch (Mock)",
    description=(
        "Ingests batch telemetry metrics produced by simulated network nodes. "
        "NOTE: Acknowledges ingestion in mock mode; data is not yet committed to a persistent database."
    ),
)
async def ingest_telemetry(payload: TelemetryBatchRequest) -> ApiResponse[TelemetryIngestResponse]:
    """Ingest simulated node telemetry batch."""
    records_count = len(payload.telemetry)

    mock_ingest = TelemetryIngestResponse(
        simulation_id=payload.simulation_id,
        records_ingested=records_count,
        received_at=utc_now(),
    )

    return ApiResponse(
        status="success",
        message=f"Successfully ingested {records_count} telemetry records in mock mode.",
        data=mock_ingest,
    )
