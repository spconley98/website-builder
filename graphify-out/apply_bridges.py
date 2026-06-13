"""Apply curated bridge edges from bridges.json into graph.json.
Re-run after any graphify rebuild to re-stitch the doc<->code islands.
Skips any bridge whose endpoints are missing (warns). Idempotent (dedups)."""
import json
import networkx as nx
from pathlib import Path

graph_path = Path('graphify-out/graph.json')
bridges_path = Path('graphify-out/bridges.json')

g = json.loads(graph_path.read_text(encoding='utf-8'))
bridges = json.loads(bridges_path.read_text(encoding='utf-8'))['bridges']
node_ids = {n['id'] for n in g['nodes']}

# component count before
def ncomp():
    G = nx.Graph()
    G.add_nodes_from(node_ids)
    for e in g['links']:
        G.add_edge(e['source'], e['target'])
    return nx.number_connected_components(G)

before = ncomp()

existing = {(e['source'], e['target']) for e in g['links']}
added, skipped = 0, []
for b in bridges:
    s, t = b['source'], b['target']
    if s not in node_ids or t not in node_ids:
        skipped.append((s, t, 'missing endpoint'))
        continue
    if (s, t) in existing or (t, s) in existing:
        continue
    g['links'].append({
        'source': s, 'target': t,
        'relation': b['relation'], 'confidence': b['confidence'],
        'confidence_score': b['confidence_score'], 'weight': 1.0,
        'bridge': True, 'source_file': 'graphify-out/bridges.json',
        'source_location': b.get('note'),
    })
    existing.add((s, t))
    added += 1

after = ncomp()
graph_path.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'Bridges added: {added}  (skipped: {len(skipped)})')
for s, t, why in skipped:
    print(f'  SKIP {s} -> {t}: {why}')
print(f'Connected components: {before} -> {after}')
