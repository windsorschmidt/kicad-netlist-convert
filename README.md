## About

Tools to convert foreign EDA netlists to KiCad (S-expression) format.

Tested with KiCad/Pcbnew version 5.1.6

## Timestamps in KiCad Netlists

When importing a netlist in KiCad, from the import dialog in the "match method" field, select the radio button titled "re-associate footprints by reference" (it's not the default), otherwise KiCad will expect to read time-stamp information stored in the netlist.
