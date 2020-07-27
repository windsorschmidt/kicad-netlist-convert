#!/bin/env python3

import sexpdata

footprint_xref = {'1206': 'Capacitor_SMD:C_1206_3216Metric'}

def do_header(state):
    print('[header section]')


def do_part(state):
    print('[parts section]')
    global gather
    gather = gather_functions['part']


def do_net(state):
    print('[net section]')


def do_signal(state):
    n = state['line'].split()[1]
    if n not in state['signals'].keys():
        state['signals'][n] = {'nodes': []}
    state['current_signal'] = n
    global gather
    gather = gather_functions['signal']


def do_end(state):
    print('[end section]')

def gather_part(state):
    value = '0'
    ref, fp = state['line'].split()
    footprint = footprint_xref[fp]
    state['parts'].append({'ref': ref, 'footprint': footprint, 'value': value})


def gather_signal(state):
    nodes = [{'ref': x.split('.')[0], 'pin':x.split('.')[1]}
             for x in state['line'].split()]

    state['signals'][state['current_signal']]['nodes'].extend(nodes)


keyword_functions = {
    '*PADS-PCB*': do_header,
    '*PART*': do_part,
    '*NET*': do_net,
    '*SIGNAL*': do_signal,
    '*END*': do_end}

gather_functions = {
    'part': gather_part,
    'signal': gather_signal}


state = {
    'parts': [],
    'signals': {}}

with open('pads_netlist.asc') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        state['line'] = line
        n = line.split()[0]
        if n in keyword_functions:
            keyword_functions[n](state)
        else:
            gather(state)

parts_sexp = []
for part in state['parts']:
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
for i, sig in enumerate(state['signals'], start=1):
    a = [sexpdata.Symbol('net'),
         [sexpdata.Symbol('code'), sexpdata.Symbol(str(i))],
         [sexpdata.Symbol('name'), sexpdata.Symbol(sig)]]
    nodes = state['signals'][sig]['nodes']
    b = [[sexpdata.Symbol('node'),
          [sexpdata.Symbol('ref'), sexpdata.Symbol(n['ref'])],
          [sexpdata.Symbol('pin'), sexpdata.Symbol(n['pin'])]] for n in nodes]
    signal_sexp.append(a + b)

sexp = [sexpdata.Symbol('export'),
        [sexpdata.Symbol('version'), sexpdata.Symbol('D')],
        [sexpdata.Symbol('components'),
         parts_sexp, lib_sexp, signal_sexp]]

print(sexpdata.dumps(sexp))
