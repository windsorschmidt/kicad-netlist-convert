#!/bin/env python3

parts = []
nets = []

fp_xref = {'1206': 'Capacitor_SMD:C_1206_3216Metric'}

with open('sample/tango.net') as f:
    for line in f:
        if line.startswith('['):
            parts.append({
                'ref': next(f).strip(),
                'footprint': fp_xref[next(f).strip()],
                'value': next(f).strip()
                })
            # parts.append({x: next(f).strip() for x in
            #               ['ref', 'footprint', 'value']})
        if line.startswith('('):
            n = {'name': next(f).strip(), 'nodes':[]}
            for line in f:
                if not line.startswith(')'):
                    a = line.strip().split(',')
                    n['nodes'].append({'ref':a[0], 'pin':a[1]})
                else:
                    nets.append(n)
                    break

import sexpdata

parts_sexp = []
for part in parts:
    a = [[sexpdata.Symbol('comp'),
         [sexpdata.Symbol('ref'), sexpdata.Symbol(part['ref'])],
         [sexpdata.Symbol('value'), sexpdata.Symbol(part['value'])],
         [sexpdata.Symbol('footprint'), sexpdata.Symbol(part['footprint'])]]]
    parts_sexp.extend(a)

lib_sexp = [sexpdata.Symbol('libraries'),
            [sexpdata.Symbol('library'),
             [sexpdata.Symbol('logical'),
              sexpdata.Symbol('Device')],
             [sexpdata.Symbol('uri'),
              sexpdata.Symbol('/usr/share/kicad/library/Device.lib')]]]

signal_sexp = [sexpdata.Symbol('nets')]
for i, sig in enumerate(nets, start=1):
    a = [sexpdata.Symbol('net'),
         [sexpdata.Symbol('code'), sexpdata.Symbol(str(i))],
         [sexpdata.Symbol('name'), sexpdata.Symbol(sig['name'])]]
    nodes = sig['nodes']
    b = [[sexpdata.Symbol('node'),
          [sexpdata.Symbol('ref'), sexpdata.Symbol(n['ref'])],
          [sexpdata.Symbol('pin'), sexpdata.Symbol(n['pin'])]] for n in nodes]
    signal_sexp.append(a + b)

sexp = [sexpdata.Symbol('export'),
        [sexpdata.Symbol('version'), sexpdata.Symbol('D')],
        [sexpdata.Symbol('components'),
         parts_sexp, lib_sexp, signal_sexp]]

print(sexpdata.dumps(sexp).replace('\.', '.'))
