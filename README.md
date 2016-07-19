"d" for "Data Tools"
====================

Data tools (or, for friends, `d`) is a command-line-first data analysis
library. The goal of the library is to make data-wrangling tasks easy
and promote code reuse. Each script is supposed to do one thing well,
following the principles of the UNIX philosophy of "doing one thing and
doing it well".

Design principles
-----------------

- The command line is your friend.
- An extra command (and pipe) is better than another argument.
- CSV and JSON get priority over other formats.
- Always think of scalability and memory issues. Favour streaming algorithms.
- DRY.

List of tools
-------------

All the tools start with the abbreviated name of `datatools`, which is `d`.

- `dbyrow` performs operations between elements of the same row.
- `dcompute` performs operations which involve one field of multiple rows (for example, the average).
- `dformat` (TO DO) translate existing formats to a standard CSV format.
- `djoin` performs equality joins between tables, both in semi-streaming and full-streaming fashions.
- `drandom` generates random integer and float values.
- `dunique` keeps unique values.
- `djsonexplorer` loads a JSON document into a Python interpreter.
