from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Generic, Optional, TypeVar
from pydantic import AwareDatetime, BaseModel, Field, StringConstraints

T = TypeVar("T")

# Strictly validated node identifier: strips whitespace, enforces 1-64 chars
NodeId = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=64),
]


class NodeStatus(str, Enum):
    """Operational status of a network node."""

    HEALTHY = "healthy"
    SUSPICIOUS = "suspicious"
    COMPROMISED = "compromised"
    QUARANTINED = "quarantined"
    OFFLINE = "offline"


class SeverityLevel(str, Enum):
    """Severity classification for anomalies, alerts, and risks."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TrustLevel(str, Enum):
    """Categorical trust rating for network nodes."""

    TRUSTED = "trusted"
    SUSPICIOUS = "suspicious"
    UNTRUSTED = "untrusted"


class SimulationState(str, Enum):
    """Execution lifecycle state of the network simulation."""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class TopologyType(str, Enum):
    """Network topology architecture for simulation."""

    MESH = "mesh"
    STAR = "star"
    RING = "ring"
    TREE = "tree"
    CUSTOM = "custom"


class AttackType(str, Enum):
    """Provisional attack categories injected by the simulation engine."""

    DDOS = "ddos"
    SYBIL = "sybil"
    BLACKHOLE = "blackhole"
    DATA_TAMPERING = "data_tampering"
    PACKET_DROP = "packet_drop"


class AttackIntensity(str, Enum):
    """Intensity scale for injected attacks."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecoveryActionType(str, Enum):
    """Provisional self-healing mitigation actions supported by recovery engine."""

    QUARANTINE_NODE = "quarantine_node"
    REROUTE_TRAFFIC = "reroute_traffic"
    RATE_LIMIT = "rate_limit"
    ROTATE_KEY = "rotate_key"
    REBOOT_NODE = "reboot_node"


class RecoveryStatus(str, Enum):
    """Status lifecycle of an executed recovery action."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


def utc_now() -> datetime:
    """Helper returning current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class ApiResponse(BaseModel, Generic[T]):
    """Standard generic API response envelope."""

    status: str = Field(default="success", description="Status indicator, defaults to 'success'")
    message: Optional[str] = Field(default=None, description="Optional informational message")
    data: T = Field(..., description="Payload data returned by the endpoint")
