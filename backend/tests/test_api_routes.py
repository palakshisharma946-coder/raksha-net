"""Focused automated tests for RAKSHA-NET API route shells.

Tests cover:
1. Every implemented endpoint's expected status code and response structure.
2. Invalid request payloads (schema validation errors -> 422).
3. Invalid query parameters (out-of-bounds bounds -> 422).
4. Existing root (/) and health (/health) endpoints remaining unchanged.
5. Mock endpoints clearly indicating their mock / simulated status.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# Ensure import paths resolve
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from backend.app.main import app
except (ImportError, ModuleNotFoundError):
    from app.main import app


async def asgi_request(
    method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
    query_string: str = "",
) -> Tuple[int, Dict[str, Any]]:
    """Lightweight ASGI test client avoiding external HTTP client dependencies."""
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method.upper(),
        "path": path,
        "raw_path": path.encode(),
        "query_string": query_string.encode(),
        "headers": [
            (b"host", b"testserver"),
            (b"content-type", b"application/json"),
        ],
    }

    body_bytes = json.dumps(body).encode() if body is not None else b""
    sent_body = False

    async def receive() -> Dict[str, Any]:
        nonlocal sent_body
        if not sent_body:
            sent_body = True
            return {"type": "http.request", "body": body_bytes, "more_body": False}
        return {"type": "http.request", "body": b"", "more_body": False}

    response_body = []
    status_code = 500

    async def send(message: Dict[str, Any]) -> None:
        nonlocal status_code
        if message["type"] == "http.response.start":
            status_code = message["status"]
        elif message["type"] == "http.response.body":
            response_body.append(message.get("body", b""))

    await app(scope, receive, send)
    full_body = b"".join(response_body).decode()
    try:
        parsed_json = json.loads(full_body) if full_body else {}
    except json.JSONDecodeError:
        parsed_json = {"raw_text": full_body}

    return status_code, parsed_json


async def run_all_tests() -> int:
    """Run all test suites and report results."""
    passed = 0
    failed = 0

    async def check(test_name: str, coro) -> None:
        nonlocal passed, failed
        try:
            await coro
            passed += 1
            print(f"PASS: {test_name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL: {test_name} -> {exc}")

    # =========================================================================
    # Suite 1: Existing Root and Health Endpoints
    # =========================================================================
    async def test_root():
        code, data = await asgi_request("GET", "/")
        assert code == 200, f"Expected 200, got {code}"
        assert data["project"] == "RAKSHA-NET"
        assert data["status"] == "online"
        assert "docs_url" in data

    async def test_health():
        code, data = await asgi_request("GET", "/health")
        assert code == 200, f"Expected 200, got {code}"
        assert data["status"] == "healthy"
        assert data["service"] == "raksha-net"

    await check("System: GET / unchanged", test_root())
    await check("System: GET /health unchanged", test_health())

    # =========================================================================
    # Suite 2: Simulation Endpoints
    # =========================================================================
    async def test_simulation_start():
        payload = {
            "topology_type": "mesh",
            "node_count": 20,
            "traffic_rate_pps": 100,
            "duration_seconds": 600,
        }
        code, data = await asgi_request("POST", "/api/v1/simulation/start", body=payload)
        assert code == 200, f"Expected 200, got {code}: {data}"
        assert data["status"] == "success"
        assert "mock" in data["message"].lower()
        assert data["data"]["state"] == "running"
        assert data["data"]["active_nodes"] == 20

    async def test_simulation_start_invalid():
        # Invalid node_count = 0 (< 1)
        code, data = await asgi_request("POST", "/api/v1/simulation/start", body={"node_count": 0})
        assert code == 422, f"Expected 422, got {code}"
        assert data["status"] == "error"

    async def test_simulation_start_extra_forbidden():
        # Misspelled parameter
        payload = {"node_count": 10, "traffic_rate": 50}
        code, data = await asgi_request("POST", "/api/v1/simulation/start", body=payload)
        assert code == 422, f"Expected 422, got {code}"

    async def test_simulation_stop():
        payload = {"simulation_id": "sim-mock-001", "force": False}
        code, data = await asgi_request("POST", "/api/v1/simulation/stop", body=payload)
        assert code == 200, f"Expected 200, got {code}"
        assert data["data"]["state"] == "stopped"

    async def test_simulation_status():
        code, data = await asgi_request("GET", "/api/v1/simulation/status", query_string="simulation_id=sim-123")
        assert code == 200, f"Expected 200, got {code}"
        assert data["data"]["simulation_id"] == "sim-123"

    async def test_simulation_attack():
        payload = {
            "attack_type": "ddos",
            "target_node_ids": ["node-1", "node-2"],
            "intensity": "high",
            "duration_seconds": 60,
        }
        code, data = await asgi_request("POST", "/api/v1/simulation/attack", body=payload)
        assert code == 200, f"Expected 200, got {code}"
        assert "mock" in data["message"].lower()
        assert data["data"]["status"] == "injected_mock"

    async def test_simulation_attack_invalid_type():
        payload = {
            "attack_type": "invalid_attack",
            "target_node_ids": ["node-1"],
        }
        code, data = await asgi_request("POST", "/api/v1/simulation/attack", body=payload)
        assert code == 422, f"Expected 422, got {code}"

    async def test_simulation_attack_empty_node_ids():
        payload = {
            "attack_type": "ddos",
            "target_node_ids": ["  "],
        }
        code, data = await asgi_request("POST", "/api/v1/simulation/attack", body=payload)
        assert code == 422, f"Expected 422, got {code}"

    async def test_simulation_telemetry():
        payload = {
            "simulation_id": "sim-mock-001",
            "timestamp": "2026-10-19T22:30:00Z",
            "telemetry": [
                {
                    "node_id": "node-1",
                    "packet_loss_rate": 0.05,
                    "latency_ms": 12.4,
                    "bytes_sent": 1024,
                    "bytes_received": 2048,
                    "cpu_load": 0.35,
                }
            ],
        }
        code, data = await asgi_request("POST", "/api/v1/simulation/telemetry", body=payload)
        assert code == 202, f"Expected 202, got {code}"
        assert data["data"]["records_ingested"] == 1

    async def test_simulation_telemetry_naive_timestamp():
        # Naive timestamp should be rejected
        payload = {
            "simulation_id": "sim-mock-001",
            "timestamp": "2026-10-19T22:30:00",
            "telemetry": [
                {
                    "node_id": "node-1",
                    "packet_loss_rate": 0.0,
                    "latency_ms": 10.0,
                    "bytes_sent": 10,
                    "bytes_received": 10,
                    "cpu_load": 0.1,
                }
            ],
        }
        code, data = await asgi_request("POST", "/api/v1/simulation/telemetry", body=payload)
        assert code == 422, f"Expected 422, got {code}"

    await check("Simulation: POST /api/v1/simulation/start valid", test_simulation_start())
    await check("Simulation: POST /api/v1/simulation/start invalid payload (422)", test_simulation_start_invalid())
    await check("Simulation: POST /api/v1/simulation/start extra field rejected (422)", test_simulation_start_extra_forbidden())
    await check("Simulation: POST /api/v1/simulation/stop valid", test_simulation_stop())
    await check("Simulation: GET /api/v1/simulation/status valid", test_simulation_status())
    await check("Simulation: POST /api/v1/simulation/attack valid", test_simulation_attack())
    await check("Simulation: POST /api/v1/simulation/attack invalid enum (422)", test_simulation_attack_invalid_type())
    await check("Simulation: POST /api/v1/simulation/attack empty node ID (422)", test_simulation_attack_empty_node_ids())
    await check("Simulation: POST /api/v1/simulation/telemetry valid", test_simulation_telemetry())
    await check("Simulation: POST /api/v1/simulation/telemetry naive timestamp (422)", test_simulation_telemetry_naive_timestamp())

    # =========================================================================
    # Suite 3: AI Engine Endpoints
    # =========================================================================
    async def test_ai_evaluate_trust():
        payload = {"node_ids": ["node-1", "node-3"]}
        code, data = await asgi_request("POST", "/api/v1/ai/evaluate-trust", body=payload)
        assert code == 200, f"Expected 200, got {code}"
        assert "mock" in data["message"].lower()
        assert len(data["data"]["scores"]) == 2

    async def test_ai_evaluate_trust_empty_list():
        code, data = await asgi_request("POST", "/api/v1/ai/evaluate-trust", body={"node_ids": []})
        assert code == 422, f"Expected 422, got {code}"

    async def test_ai_anomalies():
        code, data = await asgi_request("GET", "/api/v1/ai/anomalies", query_string="severity=high&limit=5")
        assert code == 200, f"Expected 200, got {code}"
        assert data["data"]["total"] >= 1
        for a in data["data"]["anomalies"]:
            assert a["severity"] == "high"

    async def test_ai_anomalies_invalid_limit():
        code, data = await asgi_request("GET", "/api/v1/ai/anomalies", query_string="limit=0")
        assert code == 422, f"Expected 422, got {code}"

    async def test_ai_detect_anomalies():
        payload = {"node_ids": ["node-3"], "time_window_seconds": 120}
        code, data = await asgi_request("POST", "/api/v1/ai/detect-anomalies", body=payload)
        assert code == 200, f"Expected 200, got {code}"
        assert data["data"]["total"] == 1

    await check("AI: POST /api/v1/ai/evaluate-trust valid", test_ai_evaluate_trust())
    await check("AI: POST /api/v1/ai/evaluate-trust empty list (422)", test_ai_evaluate_trust_empty_list())
    await check("AI: GET /api/v1/ai/anomalies with severity filter", test_ai_anomalies())
    await check("AI: GET /api/v1/ai/anomalies invalid limit=0 (422)", test_ai_anomalies_invalid_limit())
    await check("AI: POST /api/v1/ai/detect-anomalies valid", test_ai_detect_anomalies())

    # =========================================================================
    # Suite 4: Recovery Engine Endpoints
    # =========================================================================
    async def test_recovery_recommend():
        payload = {"anomaly_id": "anom-001", "node_id": "node-3"}
        code, data = await asgi_request("POST", "/api/v1/recovery/recommend", body=payload)
        assert code == 200, f"Expected 200, got {code}"
        assert "mock" in data["message"].lower()
        assert data["data"]["recommended_action"] == "quarantine_node"

    async def test_recovery_execute():
        payload = {
            "node_id": "node-3",
            "action_type": "quarantine_node",
            "reason": "Test quarantine of compromised node",
            "triggered_by": "admin",
        }
        code, data = await asgi_request("POST", "/api/v1/recovery/execute", body=payload)
        assert code == 200, f"Expected 200, got {code}"
        assert "mock" in data["message"].lower()
        assert data["data"]["status"] == "completed"

    async def test_recovery_execute_invalid_action():
        payload = {
            "node_id": "node-3",
            "action_type": "invalid_action",
            "reason": "bad action",
        }
        code, data = await asgi_request("POST", "/api/v1/recovery/execute", body=payload)
        assert code == 422, f"Expected 422, got {code}"

    async def test_recovery_actions():
        code, data = await asgi_request("GET", "/api/v1/recovery/actions", query_string="limit=5")
        assert code == 200, f"Expected 200, got {code}"
        assert data["data"]["total"] >= 1

    async def test_recovery_actions_invalid_limit():
        code, data = await asgi_request("GET", "/api/v1/recovery/actions", query_string="limit=101")
        assert code == 422, f"Expected 422, got {code}"

    await check("Recovery: POST /api/v1/recovery/recommend valid", test_recovery_recommend())
    await check("Recovery: POST /api/v1/recovery/execute valid", test_recovery_execute())
    await check("Recovery: POST /api/v1/recovery/execute invalid action (422)", test_recovery_execute_invalid_action())
    await check("Recovery: GET /api/v1/recovery/actions valid", test_recovery_actions())
    await check("Recovery: GET /api/v1/recovery/actions limit > 100 (422)", test_recovery_actions_invalid_limit())

    # =========================================================================
    # Suite 5: Dashboard and Network Endpoints
    # =========================================================================
    async def test_dashboard_overview():
        code, data = await asgi_request("GET", "/api/v1/dashboard/overview")
        assert code == 200, f"Expected 200, got {code}"
        assert "mock" in data["message"].lower()
        assert data["data"]["total_nodes"] == 10
        assert data["data"]["average_trust_score"] > 0.0

    async def test_dashboard_alerts():
        code, data = await asgi_request("GET", "/api/v1/dashboard/alerts", query_string="limit=2")
        assert code == 200, f"Expected 200, got {code}"
        assert len(data["data"]["alerts"]) == 2

    async def test_dashboard_alerts_invalid_limit():
        code, data = await asgi_request("GET", "/api/v1/dashboard/alerts", query_string="limit=-1")
        assert code == 422, f"Expected 422, got {code}"

    async def test_network_topology():
        code, data = await asgi_request("GET", "/api/v1/network/topology")
        assert code == 200, f"Expected 200, got {code}"
        assert len(data["data"]["nodes"]) >= 3
        assert len(data["data"]["links"]) >= 2

    async def test_network_node_detail():
        code, data = await asgi_request("GET", "/api/v1/network/nodes/node-1")
        assert code == 200, f"Expected 200, got {code}"
        assert data["data"]["node"]["id"] == "node-1"

    await check("Dashboard: GET /api/v1/dashboard/overview valid", test_dashboard_overview())
    await check("Dashboard: GET /api/v1/dashboard/alerts valid", test_dashboard_alerts())
    await check("Dashboard: GET /api/v1/dashboard/alerts limit < 1 (422)", test_dashboard_alerts_invalid_limit())
    await check("Network: GET /api/v1/network/topology valid", test_network_topology())
    await check("Network: GET /api/v1/network/nodes/{node_id} valid", test_network_node_detail())

    print(f"\n==========================================")
    print(f"Test Suite Summary: {passed} passed, {failed} failed")
    print(f"==========================================")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
