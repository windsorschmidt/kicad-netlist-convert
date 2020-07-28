#!/bin/env python3

import sys
import sexpdata

parts = []
nets = []

input_filter = str.maketrans('', '', '()')
output_filter = str.maketrans('', '', '\\')

fp_unknown = 'Symbol:Symbol_Danger_CopperTop_Small'

if len(sys.argv) < 2:
    print('usage: {} <netlist>'.format(sys.argv[0]))
    sys.exit(0)
else:
    filename = sys.argv[1]

with open(filename, encoding='iso-8859-1') as f:
    for line in f:
        if line.startswith('['):
            parts.append({
                'ref': next(f).strip(),
                'footprint': next(f).strip().translate(input_filter),
                'value': next(f).strip().translate(input_filter)
            })
        if line.startswith('('):
            n = {'name': next(f).strip(), 'nodes': []}
            for line in f:
                if not line.startswith(')'):
                    a = line.strip().split(',')
                    n['nodes'].append({'ref': a[0], 'pin': a[1]})
                else:
                    nets.append(n)
                    break


parts_sexp = [[
    sexpdata.Symbol('comp'),
    [sexpdata.Symbol('ref'), sexpdata.Symbol(part['ref'])],
    [sexpdata.Symbol('value'), sexpdata.Symbol(part['value'])],
    [sexpdata.Symbol('footprint'), sexpdata.Symbol(part['footprint'])]]
    for part in parts]

lib_sexp = [
    sexpdata.Symbol('libraries'),
    [sexpdata.Symbol('library'),
     [sexpdata.Symbol('logical'), sexpdata.Symbol('Device')],
     [sexpdata.Symbol('uri'),
      sexpdata.Symbol('/usr/share/kicad/library/Device.lib'),
      sexpdata.Symbol('/usr/share/kicad/library/Symbol.lib')]]]

signal_sexp = [sexpdata.Symbol('nets')]
for i, sig in enumerate(nets, start=1):
    signal_sexp.append(
        [sexpdata.Symbol('net'),
         [sexpdata.Symbol('code'), sexpdata.Symbol(str(i))],
         [sexpdata.Symbol('name'), sexpdata.Symbol(sig['name'])]] +
        [[sexpdata.Symbol('node'),
          [sexpdata.Symbol('ref'), sexpdata.Symbol(n['ref'])],
          [sexpdata.Symbol('pin'), sexpdata.Symbol(n['pin'])]]
         for n in sig['nodes']])

sexp = [sexpdata.Symbol('export'),
        [sexpdata.Symbol('version'), sexpdata.Symbol('D')],
        [sexpdata.Symbol('components'), parts_sexp, lib_sexp, signal_sexp]]

print(sexpdata.dumps(sexp).translate(output_filter))
