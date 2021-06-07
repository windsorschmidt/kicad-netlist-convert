## About

Tools to convert foreign EDA netlists to KiCad (S-expression) format.

Tested with KiCad/Pcbnew version 5.1.6

## Usage

Convert from Tango netlist:

```
python3 tango.py tango_netlist.net > kicad_netlist.net
```

Convert from PADS-PCB netlist:

```
python3 pads-pcb.py pads_netlist.asc > kicad_netlist.net
```

Note: PADS-PCB netlist format does not support footprint values

## Match Footprints by Reference

When importing a netlist in KiCad, from the import dialog in the "match method" field, select the radio button titled "re-associate footprints by reference" (it's not the default), otherwise KiCad will expect to read time-stamp information stored in the netlist.

## Missing Footprints

If the footprint names given in the source Tango netlist are not valid KiCad footprint names, deselect the check box "Update footprints" in the import dialog.
