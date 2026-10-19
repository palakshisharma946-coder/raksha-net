from typing import List
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from .common import (
    AttackIntensity,
    AttackType,
    NodeId,
    SimulationState,
    TopologyType,
    utc_now,
)


class SimulationStartRequest(BaseModel):
    """Request payload to initiate a new network simulation."""

    model_config = ConfigDict(extra="forbid")

    topology_type: TopologyType = Field(
        default=TopologyType.MESH,
        description="Network topology structure",
    )
    node_count: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Number of virtual nodes in the simulation (1 to 1000)",
    )
    traffic_rate_pps: int = Field(
        default=50,
        ge=1,
        le=100000,
        description="Simulated traffic rate in packets per second",
    )
    duration_seconds: int = Field(
        default=300,
        ge=1,
        le=86400,
        description="Simulation run duration in seconds (1 to 86400, max 24 hours)",
    )


class SimulationStateResponse(BaseModel):
    """Current operational state of a simulation run."""

    simulation_id: str = Field(..., min_length=1, max_length=64, description="Unique simulation run identifier")
    state: SimulationState = Field(..., description="Current lifecycle state")
    topology_type: TopologyType = Field(..., description="Active topology structure")
    active_nodes: int = Field(..., ge=0, description="Count of currently active nodes")
    started_at: AwareDatetime = Field(..., description="Timezone-aware start timestamp")
    elapsed_seconds: int = Field(default=0, ge=0, description="Elapsed simulation seconds")


class SimulationStopRequest(BaseModel):
    """Request payload to stop or cancel an active simulation."""

    model_config = ConfigDict(extra="forbid")

    simulation_id: str = Field(..., min_length=1, max_length=64, description="Target simulation identifier")
    force: bool = Field(default=False, description="Flag for immediate non-graceful termination")


class SimulationStopResponse(BaseModel):
    """Response returned upon halting a simulation."""

    simulation_id: str = Field(..., min_length=1, max_length=64, description="Terminated simulation identifier")
    state: SimulationState = Field(default=SimulationState.STOPPED, description="Final lifecycle state")
    stopped_at: AwareDatetime = Field(default_factory=utc_now, description="Timezone-aware stop timestamp")
    total_runtime_seconds: int = Field(..., ge=0, description="Total active duration in seconds")


class AttackInjectionRequest(BaseModel):
    """Request payload to inject a simulated cyber attack or network fault."""

    model_config = ConfigDict(extra="forbid")

    attack_type: AttackType = Field(..., description="Provisional attack category")
    target_node_ids: List[NodeId] = Field(..., min_length=1, description="List of target node identifiers")
    intensity: AttackIntensity = Field(default=AttackIntensity.MEDIUM, description="Attack intensity tier")
    duration_seconds: int = Field(default=60, ge=1, le=3600, description="Attack duration in seconds (1 to 3600)")


class AttackInjectionResponse(BaseModel):
    """Response confirming injection of a simulated attack."""

    attack_id: str = Field(..., min_length=1, max_length=64, description="Unique attack event identifier")
    attack_type: AttackType = Field(..., description="Provisional attack category injected")
    target_node_ids: List[NodeId] = Field(..., min_length=1, description="Targeted nodes")
    status: str = Field(default="injected", description="Current injection status")
    injected_at: AwareDatetime = Field(default_factory=utc_now, description="Timezone-aware injection timestamp")


class TelemetryRecord(BaseModel):
    """Telemetry reading reported for a single network node."""

    model_config = ConfigDict(extra="forbid")

    node_id: NodeId = Field(..., description="Reporting node identifier")
    packet_loss_rate: float = Field(..., ge=0.0, le=1.0, description="Packet loss ratio between 0.0 and 1.0")
    latency_ms: float = Field(..., ge=0.0, le=60000.0, description="Network latency in milliseconds")
    bytes_sent: int = Field(..., ge=0, description="Bytes transmitted during reporting interval")
    bytes_received: int = Field(..., ge=0, description="Bytes received during reporting interval")
    cpu_load: float = Field(..., ge=0.0, le=1.0, description="Node CPU utilization ratio between 0.0 and 1.0")


class TelemetryBatchRequest(BaseModel):
    """Batch ingestion payload pushed by the simulation engine."""

    model_config = ConfigDict(extra="forbid")

    simulation_id: str = Field(..., min_length=1, max_length=64, description="Simulation identifier")
    timestamp: AwareDatetime = Field(default_factory=utc_now, description="Timezone-aware batch timestamp")
    telemetry: List[TelemetryRecord] = Field(..., min_length=1, description="List of per-node telemetry readings")


class TelemetryIngestResponse(BaseModel):
    """Response acknowledging telemetry ingestion."""

    simulation_id: str = Field(..., min_length=1, max_length=64, description="Simulation identifier")
    records_ingested: int = Field(..., ge=0, description="Count of ingested records")
    received_at: AwareDatetime = Field(default_factory=utc_now, description="Timezone-aware ingestion timestamp")
