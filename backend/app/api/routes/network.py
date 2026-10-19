import sys
from pathlib import Path
from fastapi import APIRouter, Path as FastPath, status

# Support importing across diverse execution contexts
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from backend.app.schemas import (
        ApiResponse,
        NetworkLink,
        NetworkNode,
        NetworkTopologyResponse,
        NodeDetailResponse,
        NodeStatus,
        TrustLevel,
        utc_now,
    )
except (ImportError, ModuleNotFoundError):
    from app.schemas import (
        ApiResponse,
        NetworkLink,
        NetworkNode,
        NetworkTopologyResponse,
        NodeDetailResponse,
        NodeStatus,
        TrustLevel,
        utc_now,
    )

router = APIRouter()


@router.get(
    "/topology",
    response_model=ApiResponse[NetworkTopologyResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Network Graph Topology (Mock)",
    description=(
        "Retrieves active network graph representation (nodes and connecting links) "
        "formatted for graph visualizers (such as Cytoscape, D3, or vis.js). "
        "NOTE: Returns deterministic mock graph structure."
    ),
)
async def get_network_topology() -> ApiResponse[NetworkTopologyResponse]:
    """Retrieve full mock network topology graph."""
    mock_nodes = [
        NetworkNode(
            id="node-1",
            label="Gateway 1",
            role="gateway",
            status=NodeStatus.HEALTHY,
            trust_score=0.98,
            trust_level=TrustLevel.TRUSTED,
            ip_address="192.168.1.1",
        ),
        NetworkNode(
            id="node-2",
            label="Router 2",
            role="router",
            status=NodeStatus.HEALTHY,
            trust_score=0.92,
            trust_level=TrustLevel.TRUSTED,
            ip_address="192.168.1.2",
        ),
        NetworkNode(
            id="node-3",
            label="Sensor 3 (Compromised)",
            role="sensor",
            status=NodeStatus.COMPROMISED,
            trust_score=0.31,
            trust_level=TrustLevel.UNTRUSTED,
            ip_address="192.168.1.3",
        ),
        NetworkNode(
            id="node-4",
            label="Sensor 4 (Quarantined)",
            role="sensor",
            status=NodeStatus.QUARANTINED,
            trust_score=0.25,
            trust_level=TrustLevel.UNTRUSTED,
            ip_address="192.168.1.4",
        ),
        NetworkNode(
            id="node-5",
            label="Sensor 5",
            role="sensor",
            status=NodeStatus.HEALTHY,
            trust_score=0.89,
            trust_level=TrustLevel.TRUSTED,
            ip_address="192.168.1.5",
        ),
    ]

    mock_links = [
        NetworkLink(source="node-1", target="node-2", latency_ms=4.2, status="active"),
        NetworkLink(source="node-2", target="node-3", latency_ms=185.0, status="congested"),
        NetworkLink(source="node-2", target="node-4", latency_ms=0.0, status="blocked"),
        NetworkLink(source="node-2", target="node-5", latency_ms=12.1, status="active"),
    ]

    mock_topology = NetworkTopologyResponse(
        nodes=mock_nodes,
        links=mock_links,
        generated_at=utc_now(),
    )

    return ApiResponse(
        status="success",
        message="Network topology graph retrieved in mock mode.",
        data=mock_topology,
    )


@router.get(
    "/nodes/{node_id}",
    response_model=ApiResponse[NodeDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Node Detail Metrics (Mock)",
    description=(
        "Retrieves deep-dive operational metrics, latency, CPU utilization, and trust rating for a single node. "
        "NOTE: Returns deterministic mock operational telemetry."
    ),
)
async def get_node_detail(
    node_id: str = FastPath(
        ...,
        min_length=1,
        max_length=64,
        description="Unique node identifier to inspect",
    ),
) -> ApiResponse[NodeDetailResponse]:
    """Retrieve detailed mock metrics for target node."""
    is_compromised = "3" in node_id or "bad" in node_id.lower() or "compromised" in node_id.lower()

    base_node = NetworkNode(
        id=node_id,
        label=f"Node {node_id}",
        role="sensor",
        status=NodeStatus.COMPROMISED if is_compromised else NodeStatus.HEALTHY,
        trust_score=0.31 if is_compromised else 0.94,
        trust_level=TrustLevel.UNTRUSTED if is_compromised else TrustLevel.TRUSTED,
        ip_address="192.168.1.99",
    )

    mock_detail = NodeDetailResponse(
        node=base_node,
        packet_loss_rate=0.42 if is_compromised else 0.01,
        latency_ms=185.4 if is_compromised else 8.5,
        cpu_load=0.88 if is_compromised else 0.22,
        active_alerts_count=2 if is_compromised else 0,
        last_seen=utc_now(),
    )

    return ApiResponse(
        status="success",
        message=f"Node detail for '{node_id}' retrieved in mock mode.",
        data=mock_detail,
    )
