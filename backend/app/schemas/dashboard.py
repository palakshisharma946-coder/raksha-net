from typing import List, Optional
from pydantic import AwareDatetime, BaseModel, Field

from .common import (
    NodeId,
    NodeStatus,
    SeverityLevel,
    SimulationState,
    TrustLevel,
    utc_now,
)


class DashboardOverviewResponse(BaseModel):
    """Aggregated high-level KPI metrics for the frontend dashboard."""

    simulation_state: SimulationState = Field(
        ...,
        description="Lifecycle state of simulation (idle, running, paused, stopped)",
    )
    total_nodes: int = Field(..., ge=0, description="Total nodes currently registered in network")
    healthy_nodes: int = Field(..., ge=0, description="Count of nodes in healthy state")
    compromised_nodes: int = Field(..., ge=0, description="Count of nodes marked compromised or untrusted")
    quarantined_nodes: int = Field(..., ge=0, description="Count of isolated / quarantined nodes")
    average_trust_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Network-wide average trust score in range 0.0 to 1.0",
    )
    active_anomalies_count: int = Field(..., ge=0, description="Count of unresolved security anomalies")
    last_updated: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware metrics refresh timestamp",
    )


class NetworkNode(BaseModel):
    """Provisional graph node representation for network visualization."""

    id: NodeId = Field(..., description="Unique node identifier")
    label: str = Field(..., min_length=1, max_length=128, description="Display name or label")
    role: str = Field(
        default="sensor",
        min_length=1,
        max_length=32,
        description="Node role: e.g. 'sensor', 'router', 'gateway'",
    )
    status: NodeStatus = Field(..., description="Operational status of the node")
    trust_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Evaluated trust score in range 0.0 to 1.0",
    )
    trust_level: TrustLevel = Field(default=TrustLevel.TRUSTED, description="Categorical trust classification")
    ip_address: Optional[str] = Field(default=None, description="Optional IP address")


class NetworkLink(BaseModel):
    """Provisional graph link/edge representation connecting two nodes."""

    source: NodeId = Field(..., description="Source node identifier")
    target: NodeId = Field(..., description="Target node identifier")
    latency_ms: float = Field(..., ge=0.0, le=60000.0, description="Inter-node latency in milliseconds")
    status: str = Field(
        default="active",
        description="Link operational state: e.g. 'active', 'congested', 'severed'",
    )


class NetworkTopologyResponse(BaseModel):
    """Full network graph snapshot formatted for frontend visualizers."""

    nodes: List[NetworkNode] = Field(..., description="Collection of topology nodes")
    links: List[NetworkLink] = Field(..., description="Collection of topology links/edges")
    generated_at: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware graph generation timestamp",
    )


class NodeDetailResponse(BaseModel):
    """Deep-dive operational metrics and status for a single node."""

    node: NetworkNode = Field(..., description="Base node attributes and trust level")
    packet_loss_rate: float = Field(..., ge=0.0, le=1.0, description="Current packet loss ratio (0.0 to 1.0)")
    latency_ms: float = Field(..., ge=0.0, le=60000.0, description="Current latency in ms")
    cpu_load: float = Field(..., ge=0.0, le=1.0, description="Current CPU utilization ratio (0.0 to 1.0)")
    active_alerts_count: int = Field(default=0, ge=0, description="Count of open alerts targeting this node")
    last_seen: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware last contact timestamp",
    )


class DashboardAlert(BaseModel):
    """Security alert card rendered on the dashboard alert feed."""

    alert_id: str = Field(..., min_length=1, max_length=64, description="Unique alert identifier")
    node_id: NodeId = Field(..., description="Associated node identifier")
    severity: SeverityLevel = Field(..., description="Threat severity tier")
    title: str = Field(..., min_length=1, max_length=128, description="Brief alert headline")
    message: str = Field(..., min_length=1, max_length=500, description="Detailed alert summary")
    timestamp: AwareDatetime = Field(
        default_factory=utc_now,
        description="Timezone-aware alert creation timestamp",
    )
    is_resolved: bool = Field(default=False, description="Flag indicating if alert has been addressed")


class DashboardAlertsResponse(BaseModel):
    """Collection of dashboard security alerts."""

    total: int = Field(..., ge=0, description="Total count of alerts")
    alerts: List[DashboardAlert] = Field(..., description="List of alert items")
