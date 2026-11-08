#!/usr/bin/env python3
"""
Offline Ed25519 Execution Receipt Verifier for ProofBox (RFC 8032).
Zero network calls required.

By default, this verifier strictly pins the official ProofBox Vultr Notary Public Key
as the root of trust, rejecting any receipt signed by an unauthenticated or attacker-generated keypair.

Usage:
    python3 scripts/verify_receipt.py examples/sample_live_receipt.json
    python3 scripts/verify_receipt.py examples/sample_live_receipt.json --tamper-test
    python3 scripts/verify_receipt.py examples/sample_live_receipt.json --forged-signer-test
"""

import sys
import json
import hashlib
import argparse
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

# Ensure UTF-8 console output on Windows PowerShell / CMD
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Official pinned Ed25519 public key of the ProofBox Vultr Orchestrator Notary
PINNED_VULTR_NOTARY_PUBKEY_HEX = "ec5b7757873c502b0a4455c9108777a24b99d79efbbfd12354935cabd81bf1d0"


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_receipt_dict(
    receipt: dict,
    trust_custom_pubkey: str | None = None,
) -> tuple[bool, list[str]]:
    logs: list[str] = []
    crypto = receipt.get("cryptographicProof", {})
    lifecycle = receipt.get("containerLifecycle", {})

    receipt_id = receipt.get("receiptId", "")
    container_id = lifecycle.get("containerId", "")
    exit_code = lifecycle.get("exitCode")
    spawned_at = lifecycle.get("spawnedAt", "")
    destroyed_at = lifecycle.get("destroyedAt", "")

    # 1. Verify Signer Public Key against the Pinned Root of Trust
    receipt_pubkey_hex = crypto.get("ed25519PublicKeyHex", "")
    if trust_custom_pubkey:
        trusted_pubkey_hex = trust_custom_pubkey.strip().lower()
        logs.append(f"! WARNING: Using user-supplied custom public key override ({trusted_pubkey_hex[:24]}...).")
    else:
        trusted_pubkey_hex = PINNED_VULTR_NOTARY_PUBKEY_HEX

    if receipt_pubkey_hex.lower() != trusted_pubkey_hex:
        return False, [
            "FAIL: Untrusted Signer Public Key in receipt!",
            f"  Pinned Trusted Notary Key : {trusted_pubkey_hex}",
            f"  Receipt Embedded Key      : {receipt_pubkey_hex}",
            "  (Signature may be mathematically self-consistent, but signer is NOT the trusted Vultr Notary.)",
        ]
    logs.append(f"✓ Signer public key matches pinned Vultr Notary key ({trusted_pubkey_hex[:24]}...).")

    # 2. Recompute SHA-256 digests of prompt, executed code, and stdout
    calc_input_sha = sha256_hex(receipt.get("prompt", ""))
    calc_code_sha = sha256_hex(receipt.get("generatedCode", ""))
    calc_stdout_sha = sha256_hex(receipt.get("stdout", ""))

    if calc_input_sha != crypto.get("inputSha256"):
        return False, [*logs, f"FAIL: inputSha256 mismatch (calculated {calc_input_sha} != {crypto.get('inputSha256')})"]
    if calc_code_sha != crypto.get("codeSha256"):
        return False, [*logs, f"FAIL: codeSha256 mismatch (calculated {calc_code_sha} != {crypto.get('codeSha256')})"]
    if calc_stdout_sha != crypto.get("stdoutSha256"):
        return False, [*logs, f"FAIL: stdoutSha256 mismatch (calculated {calc_stdout_sha} != {crypto.get('stdoutSha256')})"]
    logs.append("✓ SHA-256 digests verified for prompt, generatedCode, and stdout.")

    # 3. Reconstruct canonical JSON payload and compare with canonicalPayloadJson
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
            *logs,
            "FAIL: canonicalPayloadJson does not match receipt fields.",
            f"  Expected: {expected_canonical_json}",
            f"  Stored:   {stored_canonical_json}",
        ]
    logs.append("✓ Canonical JSON payload matches receipt lifecycle & digest fields.")

    # 4. Verify Ed25519 signature (RFC 8032) using the Pinned Trusted Public Key
    sig_hex = crypto.get("receiptSignatureSha256", "")
    try:
        pub_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(trusted_pubkey_hex))
        pub_key.verify(bytes.fromhex(sig_hex), stored_canonical_json.encode("utf-8"))
        logs.append("✓ Ed25519 signature mathematically verified against pinned public key.")
    except Exception as exc:
        return False, [*logs, f"FAIL: Ed25519 signature verification failed ({exc!r})"]

    # 5. Report Multi-Dimensional Task Status alongside Receipt Integrity
    artifacts = receipt.get("artifacts", [])
    exec_state = "COMPLETED (Exit 0)" if exit_code == 0 else f"NON-ZERO EXIT ({exit_code})"
    goal_state = (
        f"MET ({len(artifacts)} artifact(s) + non-empty stdout)"
        if (exit_code == 0 and len(receipt.get("stdout", "").strip()) > 0)
        else "CONTAINED / BLOCKED OR PARTIAL"
    )
    logs.append(f"• Execution State : {exec_state}")
    logs.append(f"• Goal State      : {goal_state}")
    logs.append("• Receipt State   : VALID & UNTAMPERED")

    return True, logs


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline Ed25519 Receipt Verifier for ProofBox")
    parser.add_argument("receipt_file", help="Path to exported ProofReceipt JSON file")
    parser.add_argument(
        "--trust-custom-pubkey",
        help="Explicitly override the pinned Vultr Notary public key hex (use only for custom deployments)",
        default=None,
    )
    parser.add_argument(
        "--tamper-test",
        action="store_true",
        help="Flip 1 character in stdout after loading to prove tamper detection fails verification",
    )
    parser.add_argument(
        "--forged-signer-test",
        action="store_true",
        help="Re-sign receipt with a newly generated attacker Ed25519 keypair to prove pinned-key verification rejects untrusted signers",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.receipt_file).read_text(encoding="utf-8"))
    if args.tamper_test:
        print("[TAMPER TEST] Modifying 1 byte of receipt['stdout'] in memory...")
        data["stdout"] = data.get("stdout", "") + "X"

    if args.forged_signer_test:
        print("[FORGED SIGNER TEST] Generating attacker Ed25519 keypair and re-signing receipt...")
        attacker_priv = Ed25519PrivateKey.generate()
        attacker_pub_hex = attacker_priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()
        canon_bytes = data["cryptographicProof"]["canonicalPayloadJson"].encode("utf-8")
        data["cryptographicProof"]["ed25519PublicKeyHex"] = attacker_pub_hex
        data["cryptographicProof"]["receiptSignatureSha256"] = attacker_priv.sign(canon_bytes).hex()

    ok, messages = verify_receipt_dict(data, args.trust_custom_pubkey)
    for m in messages:
        print(" ", m)

    if ok:
        print(
            f"\nVERDICT: VALID ED25519 RECEIPT ({data.get('receiptId')} · Container {data.get('containerLifecycle', {}).get('containerId')})"
        )
        return 0
    else:
        print(f"\nVERDICT: INVALID / UNTRUSTED / TAMPERED RECEIPT ({data.get('receiptId')})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
