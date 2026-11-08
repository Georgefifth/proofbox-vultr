#!/usr/bin/env python3
"""
Offline Ed25519 Execution Receipt Verifier for ProofBox (RFC 8032).
Zero network calls required.

Usage:
    python3 scripts/verify_receipt.py examples/sample_live_receipt.json
    python3 scripts/verify_receipt.py examples/sample_live_receipt.json --tamper-test
"""

import sys
import json
import hashlib
import argparse
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DEFAULT_ORCHESTRATOR_PUBKEY_HEX = "ec5b7757873c502b0a4455c9108777a24b99d79efbbfd12354935cabd81bf1d0"


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_receipt_dict(receipt: dict, pubkey_override: str | None = None) -> tuple[bool, list[str]]:
    logs: list[str] = []
    crypto = receipt.get("cryptographicProof", {})
    lifecycle = receipt.get("containerLifecycle", {})

    receipt_id = receipt.get("receiptId", "")
    container_id = lifecycle.get("containerId", "")
    exit_code = lifecycle.get("exitCode")
    spawned_at = lifecycle.get("spawnedAt", "")
    destroyed_at = lifecycle.get("destroyedAt", "")

    # 1. Recompute SHA-256 digests of prompt, executed code, and stdout
    calc_input_sha = sha256_hex(receipt.get("prompt", ""))
    calc_code_sha = sha256_hex(receipt.get("generatedCode", ""))
    calc_stdout_sha = sha256_hex(receipt.get("stdout", ""))

    if calc_input_sha != crypto.get("inputSha256"):
        return False, [f"FAIL: inputSha256 mismatch (calculated {calc_input_sha} != {crypto.get('inputSha256')})"]
    if calc_code_sha != crypto.get("codeSha256"):
        return False, [f"FAIL: codeSha256 mismatch (calculated {calc_code_sha} != {crypto.get('codeSha256')})"]
    if calc_stdout_sha != crypto.get("stdoutSha256"):
        return False, [f"FAIL: stdoutSha256 mismatch (calculated {calc_stdout_sha} != {crypto.get('stdoutSha256')})"]
    logs.append("✓ SHA-256 digests verified for prompt, generatedCode, and stdout.")

    # 2. Reconstruct canonical JSON payload and compare with canonicalPayloadJson
    expected_canonical_obj = {
        "receiptId": receipt_id,
        "containerId": container_id,
        "inputSha256": calc_input_sha,
        "codeSha256": calc_code_sha,
        "stdoutSha256": calc_stdout_sha,
        "exitCode": exit_code,
        "spawnedAt": spawned_at,
        "destroyedAt": destroyed_at,
    }
    expected_canonical_json = json.dumps(expected_canonical_obj, sort_keys=True, separators=(",", ":"))
    stored_canonical_json = crypto.get("canonicalPayloadJson", "")

    if stored_canonical_json != expected_canonical_json:
        return False, [
            "FAIL: canonicalPayloadJson does not match receipt fields.",
            f"  Expected: {expected_canonical_json}",
            f"  Stored:   {stored_canonical_json}",
        ]
    logs.append("✓ Canonical JSON payload matches receipt lifecycle & digest fields.")

    # 3. Verify Ed25519 signature (RFC 8032) using public key
    pub_hex = pubkey_override or crypto.get("ed25519PublicKeyHex") or DEFAULT_ORCHESTRATOR_PUBKEY_HEX
    sig_hex = crypto.get("receiptSignatureSha256", "")

    try:
        pub_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))
        pub_key.verify(bytes.fromhex(sig_hex), stored_canonical_json.encode("utf-8"))
        logs.append(f"✓ Ed25519 signature verified against public key {pub_hex[:24]}...")
    except Exception as exc:
        return False, [*logs, f"FAIL: Ed25519 signature verification failed ({exc!r})"]

    return True, logs


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline Ed25519 Receipt Verifier for ProofBox")
    parser.add_argument("receipt_file", help="Path to exported ProofReceipt JSON file")
    parser.add_argument("--pubkey", help="Optional Ed25519 public key hex override", default=None)
    parser.add_argument(
        "--tamper-test",
        action="store_true",
        help="Flip 1 character in stdout after loading to prove tamper detection fails verification",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.receipt_file).read_text(encoding="utf-8"))
    if args.tamper_test:
        print("[TAMPER TEST] Modifying 1 byte of receipt['stdout'] in memory...")
        data["stdout"] = data.get("stdout", "") + "X"

    ok, messages = verify_receipt_dict(data, args.pubkey)
    for m in messages:
        print(" ", m)

    if ok:
        print(f"\nVERDICT: VALID ED25519 RECEIPT ({data.get('receiptId')} · Container {data.get('containerLifecycle', {}).get('containerId')})")
        return 0
    else:
        print(f"\nVERDICT: INVALID / TAMPERED RECEIPT ({data.get('receiptId')})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
