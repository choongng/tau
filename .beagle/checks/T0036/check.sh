#!/bin/bash
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_tau_ai.py 1 test_qwen_chat_template_thinking_off_disables_in_payload
python3 - <<'P'
import tomllib, os
c = tomllib.load(open(os.path.expanduser('~/.tau/catalog.toml'), 'rb'))
found = {}
for prov in c.get('providers', []):
    for i, d in (prov.get('model_metadata') or {}).items():
        if i in ('mimo-v2.6-9b-q4', 'qwen3.5-9b-q4-mtp-thinking-coding'):
            assert d.get('thinking_level_map', {}).get('off') == 'none', (i, d)
            assert d.get('compat', {}).get('thinkingFormat') == 'qwen-chat-template', (i, d)
            found[i] = True
assert len(found) == 2, found
print('OK catalog')
P
