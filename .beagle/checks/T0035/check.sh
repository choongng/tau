#!/bin/bash
set -eu
H=/home/choong/tautest/itc-harness
S=$(python3 -c "import json;print(json.load(open('$H/runs/R02/meta.json'))['session'])")
python3 $H/scorecard.py --session "$S" --repo /home/choong/itc.r02 --meta $H/runs/R02/meta.json --json > /tmp/claude-1000/sc-T0035.json
python3 - <<'P'
import json; s=json.load(open('/tmp/claude-1000/sc-T0035.json'))
w=s['workers']; assert w['count']==17, w
for k in ('turns_max','capped','timed_out','reasoning_chars','empty_reports'): assert k in w, k
assert s['ended_with_abandoned'] is True, s.get('ended_with_abandoned')
print('OK')
P
python3 - <<'P'
import sys; sys.path.insert(0,'/home/choong/tautest/itc-harness'); import scorecard as s
card={'ended':'finished','tasks_abandoned':1}
mk=lambda i,st,**k: dict(id=i,parent=k.get('parent','T0001'),status=st,sibling_of=k.get('sib',''),reason=k.get('reason',''))
root=mk('T0001','pending',parent='')
assert s.ended_with_abandoned(card,{'nodes':[root,mk('T0002','abandoned'),mk('T0003','done',sib='T0002')]}) is False
assert s.ended_with_abandoned(card,{'nodes':[root,mk('T0002','abandoned',reason='duplicate of T0003'),mk('T0003','done')]}) is False
assert s.ended_with_abandoned(card,{'nodes':[root,mk('T0002','abandoned',reason='already done')]}) is True
print('OK successors')
P
