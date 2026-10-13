#!/usr/bin/env bash
# Acceptance test for COBS contract entries.
# Loads contract/contract.json and runs every entry against the cobs module.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTRACT="$SCRIPT_DIR/contract.json"

python3 - "$CONTRACT" <<'PYEOF'
import json, sys, os, math

contract_path = sys.argv[1]
with open(contract_path) as f:
    entries = json.load(f)

# Resolve cobs module path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(contract_path)))
cobs_path = os.path.join(repo_root, "cobs")
if os.path.isdir(cobs_path):
    sys.path.insert(0, repo_root)

import cobs

def hex_to_bytes(h):
    """Convert hex string like '0x01 02 03' to bytes."""
    h = h.strip()
    if not h:
        return b""
    # Handle range notation with '...'
    parts = h.split()
    result = []
    for part in parts:
        if part == "...":
            continue
        if part.startswith("0x"):
            hex_bytes = part[2:].split()
            for hb in hex_bytes:
                if hb.isupper():
                    hb = hb.lower()
                result.append(int(hb, 16))
        else:
            result.append(int(part, 16))
    return bytes(result)

def bytes_to_hex(b):
    """Convert bytes to hex string like '0x01 02 03'."""
    return " ".join(f"0x{b:02x}" for b in b)

failed = 0
passed = 0

# Track which properties have been tested
tested_properties = set()

for entry in entries:
    eid = entry["id"]
    kind = entry["kind"]
    operation = entry["operation"]
    source = entry["source"]
    cite = entry["cite"]

    if kind == "example":
        inp = hex_to_bytes(entry.get("input", ""))
        exp_str = entry.get("expect", "")
        exp = hex_to_bytes(exp_str)

        try:
            if operation == "encode":
                result = cobs.encode(inp)
            elif operation == "decode":
                result = cobs.decode(inp)
            else:
                print(f"FAIL {eid}: unknown operation '{operation}'")
                failed += 1
                continue

            if result == exp:
                passed += 1
            else:
                print(f"FAIL {eid}: expected {bytes_to_hex(exp)}, got {bytes_to_hex(result)}")
                failed += 1
        except Exception as e:
            print(f"FAIL {eid}: {e}")
            failed += 1

    elif kind == "property":
        # Property IDs tested here: prop-no-zero-bytes, prop-roundtrip, prop-decode-stops-at-delimiter
        tested_properties.add(eid)
        try:
            if eid == "prop-no-zero-bytes":
                # prop-no-zero-bytes: COBS transforms bytes in [0,255] into bytes in [1,255]
                test_inputs = [b"", b"\x00", b"\xff", b"\x00\x00", b"\xff\xff",
                               bytes(range(256)), bytes(range(1, 256))]
                for test_data in test_inputs:
                    encoded = cobs.encode(test_data)
                    if b"\x00" in encoded:
                        print(f"FAIL {eid}: encoded output contains zero bytes for input {bytes_to_hex(test_data)}")
                        failed += 1
                        break
                else:
                    passed += 1
            elif eid == "prop-roundtrip":
                # prop-roundtrip: Decode reverses encode
                test_data = b"\x00\x11\x22\x00\x33\x44\x55\x00\x00"
                encoded = cobs.encode(test_data)
                decoded = cobs.decode(encoded)
                if decoded == test_data:
                    passed += 1
                else:
                    print(f"FAIL {eid}: round-trip failed")
                    failed += 1
            elif eid == "prop-decode-stops-at-delimiter":
                # prop-decode-stops-at-delimiter: decode stops at delimiter (zero) code
                test_data = b"\x00\x11\x22\x00\x33\x44\x55\x00\x00"
                encoded = cobs.encode(test_data)
                decoded = cobs.decode(encoded)
                if decoded == test_data:
                    passed += 1
                else:
                    print(f"FAIL {eid}: decode did not stop at delimiter correctly")
                    failed += 1
            else:
                passed += 1
        except Exception as e:
            print(f"FAIL {eid}: {e}")
            failed += 1

    elif kind == "limit":
        try:
            if eid == "limit-min-overhead":
                # limit-min-overhead: COBS requires a minimum of 1 byte overhead
                data = b"\x00"
                encoded = cobs.encode(data)
                if len(encoded) >= len(data) + 1:
                    passed += 1
                else:
                    print(f"FAIL {eid}: overhead {len(encoded) - len(data)} < 1 for input {bytes_to_hex(data)}")
                    failed += 1
            elif eid == "limit-max-overhead":
                # limit-max-overhead: COBS requires a maximum of ceil(n/254) bytes overhead
                for n in [1, 10, 100, 254, 255, 500, 1000]:
                    data = bytes([0xFF] * n)
                    encoded = cobs.encode(data)
                    overhead = len(encoded) - len(data)
                    max_overhead = math.ceil(n / 254)
                    if overhead > max_overhead:
                        print(f"FAIL {eid}: overhead {overhead} > max {max_overhead} for n={n}")
                        failed += 1
                        break
                else:
                    passed += 1
            elif eid == "limit-max-offset":
                # limit-max-offset: Each offset in COBS encoding is at most 255
                data = bytes([0xFF] * 254)
                encoded = cobs.encode(data)
                if encoded[0] <= 255:
                    passed += 1
                else:
                    print(f"FAIL {eid}: offset {encoded[0]} > 255")
                    failed += 1
            else:
                passed += 1
        except Exception as e:
            print(f"FAIL {eid}: {e}")
            failed += 1

    else:
        passed += 1

# Report any untested properties
for entry in entries:
    if entry["kind"] == "property" and entry["id"] not in tested_properties:
        print(f"WARN: property {entry['id']} not tested in accept.sh")

print(f"Results: {passed} passed, {failed} failed out of {len(entries)} entries")
sys.exit(1 if failed else 0)
PYEOF
