#!/usr/bin/env python3
"""
从 community_verified.json 生成 shields.io endpoint JSON。
用法: python3 generate_badges.py
"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(SCRIPT_DIR, '..', '..', 'jade-core', 'jade_registry', 'community_verified.json')
OUT_DIR = os.path.join(SCRIPT_DIR, '..', 'api', 'badge')

SEAL = {
    '💠': ('💠 Origin Verified', '10b981'),
    '🔷': ('🔷 Org Verified', '3b82f6'),
    '🔹': ('🔹 Community Verified', '10b981'),
}

with open(REGISTRY) as f:
    reg = json.load(f)

n = 0
for key, entry in reg.items():
    if key.startswith('_') or not entry.get('verified'):
        continue
    parts = key.split('/')
    if len(parts) != 2:
        continue
    org, repo = parts
    seal = entry.get('seal', '🔹')
    msg, color = SEAL.get(seal, SEAL['🔹'])
    
    out_dir = os.path.join(OUT_DIR, org)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f'{repo}.json'), 'w') as f:
        json.dump({'schemaVersion': 1, 'label': 'JadeGate', 'message': msg, 'color': color, 'style': 'flat-square'}, f, indent=2, ensure_ascii=False)
    n += 1
    print(f'  ✅ {key}')

print(f'\nGenerated {n} badge(s)')
