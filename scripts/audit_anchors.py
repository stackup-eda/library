"""Audit library-owned passive placements and verify anchor pin/package mappings.

This source audit reads the KDL statement subset used by this library. Stackup
check/netlist remains authoritative for elaboration, parameter forwarding, and
conditional application blocks. Run from any directory; no KiCad dependency.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\\[ \t]*\n|[\n;{}=]|[^\s;{}=]+')


def parse(text):
    root = {'t': [], 'children': [], 'parent': None}
    current, pending = root, []
    for match in TOKEN.finditer(text):
        value = match.group()
        if value.startswith(('//', '/*', '\\')):
            continue
        if value in ('\n', ';', '{', '}'):
            if pending:
                node = {'t': [item[0] for item in pending],
                        'start': pending[0][1], 'end': pending[-1][2],
                        'children': [], 'parent': current}
                current['children'].append(node)
                pending = []
                if value == '{':
                    current = node
            if value == '}':
                current = current['parent']
        else:
            pending.append((value, match.start(), match.end()))
    return root


def val(token):
    return json.loads(token) if token.startswith('"') else token


def props(node):
    tokens = node['t']
    return {tokens[i - 1]: val(tokens[i + 1]) for i in range(1, len(tokens) - 1)
            if tokens[i] == '='}


def walk(node):
    for child in node['children']:
        yield child
        yield from walk(child)


files = {path: parse(path.read_text()) for path in ROOT.rglob('*.kdl')
         if 'examples' not in path.parts and '.stackup' not in path.parts}
defs = {val(node['t'][1]): node for root in files.values() for node in root['children']
        if node['t'][0] in ('part', 'block')}


def ancestors(node):
    while node['parent']:
        node = node['parent']
        yield node


def pins(part):
    return {val(child['t'][1]) for child in part['children']
            if child['t'][0] == 'pin'} if part else set()


PASSIVES = {'decouple', 'bypass', 'bulk', 'filter', 'pull-up', 'pull-down',
            'capacitor', 'resistor', 'inductor', 'ferrite-bead', 'crystal-3225'}
# A net/contract alone cannot identify the physical host pad. These placements
# deliberately need a board layout decision; adding a new exception needs review.
EXCEPTIONS = {
    ('types.kdl', 'sda'): 'generic I2C contract; caller chooses controller/device end',
    ('types.kdl', 'scl'): 'generic I2C contract; caller chooses controller/device end',
    ('sensor/current/ina226.kdl', 'Rshunt'): 'load-current path and Kelvin routing determine location',
    ('sensor/current/ina237.kdl', 'Rshunt'): 'load-current path and Kelvin routing determine location',
    ('sensor/current/ina240.kdl', 'Rshunt'): 'load-current path and Kelvin routing determine location',
    ('power/buck/lm5146.kdl', 'Cin1'): 'selectable power FET; input bank belongs at its drain/source loop',
    ('power/buck/lm5146.kdl', 'Cin2'): 'selectable power FET; input bank belongs at its drain/source loop',
    ('power/buck/lm5146.kdl', 'Cin-hf1'): 'selectable power FET; input bank belongs at its drain/source loop',
    ('power/buck/lm5146.kdl', 'Cin-hf2'): 'selectable power FET; input bank belongs at its drain/source loop',
}

def resolve(n, reference):
    """Find a physical pin in the placement's enclosing lexical scopes."""
    base, _, pad = reference.partition('@')
    if '.' not in base:
        for scope in ancestors(n):
            if scope['t'] and scope['t'][0] == 'part' and base in pins(scope):
                return scope, base, pad
        raise ValueError('unresolved host pin ' + reference)
    instance, pin = base.split('.', 1)
    for scope in ancestors(n):
        for placed in scope['children']:
            if placed['t'][0] != 'place':
                continue
            if (instance == 'self' and props(placed).get('as') == 'self') or val(placed['t'][2]) == instance:
                part = defs.get(placed['t'][1])
                if part is None or pin not in pins(part):
                    raise ValueError('anchor must name a physical pin: ' + reference)
                return part, pin, pad
    raise ValueError('unresolved host placement ' + reference)

def audit():
    rows, errors, used = [], [], set()
    for helper in ('decouple', 'bypass', 'bulk', 'filter', 'pull-up', 'pull-down'):
        children = defs[helper]['children']
        if not any(c['t'][:3] == ['param', 'anchor', 'reference']
                   and props(c).get('default') == '#null' for c in children):
            errors.append(helper + ': missing nullable anchor parameter')
        if not any(c['t'][0] == 'place' and props(c).get('as') == 'self'
                   and props(c).get('anchor') == 'anchor' for c in children):
            errors.append(helper + ': root passive does not forward anchor')
    for path, root in sorted(files.items()):
        for node in walk(root):
            if node['t'][0] != 'place' or node['t'][1] not in PASSIVES:
                continue
            properties = props(node)
            if properties.get('as') == 'self':
                continue
            relative = str(path.relative_to(ROOT))
            name = val(node['t'][2])
            reference = properties.get('anchor')
            line = path.read_text()[:node['start']].count('\n') + 1
            label = f'{relative}:{line} ({name})'
            reason = EXCEPTIONS.get((relative, name))
            rows.append({'file': relative, 'line': line, 'id': name,
                         'kind': node['t'][1], 'anchor': reference, 'exception': reason})
            if not reference:
                if reason:
                    used.add((relative, name))
                else:
                    errors.append(label + ': missing anchor')
                continue
            if reason:
                errors.append(label + ': stale exception')
            try:
                part, pin, selected = resolve(node, reference)
                packages = [c for c in part['children'] if c['t'][0] == 'package']
                # A package-gated block only needs a pad in that package.
                gates = [val(c['t'][1]) for a in ancestors(node) for c in a['children']
                         if c['t'][0] == 'when' and len(c['t']) == 2]
                package_gates = [m.group(1) for gate in gates
                                 if (m := re.fullmatch(r'package == ([A-Za-z0-9_-]+)', gate))]
                for package in packages:
                    if any(scope is part for scope in ancestors(node)) and package_gates and val(package['t'][1]) not in package_gates:
                        continue
                    labels = {val(c['t'][2]) for c in package['children']
                              if c['t'][0] == 'pad' and val(c['t'][1]) == pin}
                    if (selected and selected not in labels) or (not selected and len(labels) != 1):
                        raise ValueError(f'{reference}: package {package["t"][1]} has pads {sorted(labels)}; select a valid unique pad')
                if not packages:
                    raise ValueError('host has no package')
            except ValueError as error:
                errors.append(label + ': ' + str(error))
    for key in EXCEPTIONS.keys() - used:
        if not any(r['file'] == key[0] and r['id'] == key[1] for r in rows):
            errors.append(str(key) + ': exception placement no longer exists')
    for error in errors:
        print(error, file=sys.stderr)
    print(f'{len(rows)} passive placements: {sum(bool(r["anchor"]) for r in rows)} anchored, '
          f'{len(used)} reviewed exceptions, {len(errors)} errors', file=sys.stderr)
    return rows, errors

if __name__ == '__main__':
    rows, errors = audit()
    if '--json' in sys.argv:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            if row['exception']:
                print(f'{row["file"]}: {row["id"]}: {row["exception"]}')
    sys.exit(bool(errors))
