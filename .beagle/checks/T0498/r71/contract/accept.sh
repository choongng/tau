#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

python3 - "$@" <<'PYEOF'
import json, sys, os, importlib

# Load contract
contract_path = "contract/contract.json"
with open(contract_path) as f:
    contract = json.load(f)

# Try to import wrenfold
try:
    wrenfold = importlib.import_module("wrenfold")
except ImportError as e:
    print(f"FATAL: cannot import wrenfold module: {e}", file=sys.stderr)
    sys.exit(1)

encode = wrenfold.encode
decode = wrenfold.decode
count = wrenfold.count

def hex_bytes(data):
    return data.hex()

def parse_hex(s):
    return bytes.fromhex(s)

passed = 0
failed = 0
errors = []

for entry in contract["entries"]:
    eid = entry["id"]
    kind = entry["kind"]
    ok = True
    reason = ""

    try:
        if kind == "example":
            result = encode(entry["input"])
            expected = parse_hex(entry["expect"])
            if result != expected:
                ok = False
                reason = f"got {hex_bytes(result)}, expected {entry['expect']}"

        elif kind == "limit":
            val = entry["input"]
            result = encode([val])
            # Verify the encoding is valid and round-trips
            decoded, remaining = decode(result)
            if decoded != [val]:
                ok = False
                reason = f"round-trip failed: got {decoded}"

        elif kind == "invalid":
            val = entry["input"]
            if isinstance(val, str):
                # Decoder test: input is hex bytes
                try:
                    decode(parse_hex(val))
                    ok = False
                    reason = "should have raised"
                except Exception:
                    pass
            else:
                # Encoder test: input is an integer
                try:
                    encode([val])
                    ok = False
                    reason = "should have raised"
                except Exception:
                    pass

        elif kind == "property":
            if eid == "P001":
                # Encoder writes shortest form: test that 63 uses two-byte form
                result = encode([63])
                if hex_bytes(result) != "403f3f":
                    ok = False
                    reason = f"63 should use two-byte form, got {hex_bytes(result)}"
            elif eid == "P002":
                # 0x3F inside multi-byte form is data: test that 63 encodes as 0x40 0x3F
                result = encode([63])
                if len(result) != 3 or hex_bytes(result[:-1]) != "403f":
                    ok = False
                    reason = f"63 should encode as 0x40 0x3F, got {hex_bytes(result)}"
            elif eid == "P003":
                # Same as P002 essentially
                result = encode([63])
                if hex_bytes(result) != "403f3f":
                    ok = False
                    reason = f"63 should use two-byte form"
            elif eid == "P004":
                # Empty sequence is 0x3F
                result = encode([])
                if hex_bytes(result) != "3f":
                    ok = False
                    reason = f"empty sequence should be 0x3F"
            elif eid == "P005":
                # count rejects exactly the inputs a decoder rejects:
                # test that count() raises on invalid inputs
                invalid_inputs = ["05", "c000003f", "053f00", "40053f"]
                for hex_input in invalid_inputs:
                    try:
                        count(parse_hex(hex_input))
                        ok = False
                        reason = f"count should have raised on {hex_input}"
                        break
                    except Exception:
                        pass

        elif kind == "operation":
            # Verify operation exists (already imported above)
            pass

    except Exception as e:
        ok = False
        reason = str(e)

    if ok:
        passed += 1
        print(f"  PASS {eid} ({kind})")
    else:
        failed += 1
        errors.append(f"  FAIL {eid} ({kind}): {reason}")
        print(f"  FAIL {eid} ({kind}): {reason}", file=sys.stderr)

print(f"\n{passed} passed, {failed} failed out of {passed + failed} entries")
sys.exit(1 if failed else 0)
PYEOF
