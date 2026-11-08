"""
ProofBox Python SDK — Zero-Blast-Radius Ephemeral Sandbox Client for AI Agents
Compatible with Vultr Serverless Inference (https://api.vultrinference.com/v1) & OpenAI Tool Calling.
"""

from __future__ import annotations
import json
import hmac
import hashlib
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SandboxArtifact:
    name: str
    type: str
    sha256: str
    size_bytes: int
    preview_data: Optional[str] = None


@dataclass
class SandboxResult:
    receipt_id: str
    container_id: str
    status: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    cleanup_verified: bool
    secrets_injected: int
    receipt_signature_sha256: str
    artifacts: List[SandboxArtifact]
    raw_receipt: Dict[str, Any]


class Sandbox:
    """
    Programmatic client for ProofBox Ephemeral Container Sandboxes on Vultr.

    Usage:
        from sdk.proofbox import Sandbox

        sbx = Sandbox(base_url="http://45.32.110.141")
        result = sbx.exec_code(
            code="import pandas as pd; df = pd.read_csv('/workspace/data.csv'); print(df.describe().to_json())",
            files={"data.csv": "region,latency_ms\\nsgp,12\\newr,44\\nfra,38\\n"},
            air_gapped=True,
        )
        print(result.stdout)
        print("Container destroyed:", result.cleanup_verified)
        print("Ed25519 Receipt Signature:", result.receipt_signature_sha256)
    """

    def __init__(self, base_url: str = "http://45.32.110.141", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def __enter__(self) -> "Sandbox":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def exec_code(
        self,
        code: str,
        files: Optional[Dict[str, str]] = None,
        air_gapped: bool = True,
        memory_mb: int = 512,
        timeout_sec: int = 15,
    ) -> SandboxResult:
        """Execute raw Python or Playwright code inside an isolated ephemeral container."""
        payload = {
            "code": code,
            "files": files or {},
            "air_gapped": air_gapped,
            "memory_mb": memory_mb,
            "timeout_sec": timeout_sec,
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/v1/sandboxes/exec",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "ProofBox-Python-SDK/1.0"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return self._parse_receipt(data)

    def run_agent_task(
        self,
        prompt: str,
        mode: str = "code_sandbox",
        files: Optional[Dict[str, str]] = None,
        target_url: Optional[str] = None,
        air_gapped: bool = True,
    ) -> SandboxResult:
        """Plan, gate, execute, self-heal, and verify an agent task via Vultr Serverless Inference."""
        payload = {
            "prompt": prompt,
            "mode": mode,
            "files": files or {},
            "targetUrl": target_url,
            "airGapped": air_gapped,
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/execute",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "ProofBox-Python-SDK/1.0"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return self._parse_receipt(data)

    @staticmethod
    def openai_tool_schema() -> Dict[str, Any]:
        """Returns an OpenAI / Vultr Serverless Inference compatible function tool definition."""
        return {
            "type": "function",
            "function": {
                "name": "proofbox_exec_sandbox",
                "description": (
                    "Execute untrusted Python data analysis or headless Playwright browser code inside "
                    "an ephemeral, unprivileged, zero-secret Docker container on Vultr and return a "
                    "cryptographically signed Execution Proof Receipt."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Executable Python 3.12 code (supports pandas, numpy, matplotlib, playwright). Save plots/files to /output/.",
                        },
                        "air_gapped": {
                            "type": "boolean",
                            "description": "True to enforce --network=none (0 bytes egress); False only when inspecting a public web URL.",
                        },
                    },
                    "required": ["code"],
                },
            },
        }

    @staticmethod
    def _parse_receipt(data: Dict[str, Any]) -> SandboxResult:
        lifecycle = data.get("containerLifecycle", {})
        crypto = data.get("cryptographicProof", {})
        artifacts = [
            SandboxArtifact(
                name=a.get("name", ""),
                type=a.get("type", ""),
                sha256=a.get("sha256", ""),
                size_bytes=int(a.get("sizeBytes", 0)),
                preview_data=a.get("previewData"),
            )
            for a in data.get("artifacts", [])
        ]
        return SandboxResult(
            receipt_id=data.get("receiptId", ""),
            container_id=lifecycle.get("containerId", ""),
            status=data.get("status", ""),
            exit_code=int(lifecycle.get("exitCode", -1)),
            stdout=data.get("stdout", ""),
            stderr=data.get("stderr", ""),
            duration_ms=int(data.get("totalDurationMs", 0)),
            cleanup_verified=bool(lifecycle.get("cleanupVerified", False)),
            secrets_injected=int(lifecycle.get("secretsInjected", 0)),
            receipt_signature_sha256=crypto.get("receiptSignatureSha256", ""),
            artifacts=artifacts,
            raw_receipt=data,
        )
