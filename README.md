Data Tools
==========

Data tools is a commandline-first library, written in Python which makes data-wrangling easy.

Design principles
-----------------

- The command line is your friend.
- An extra command (and pipe) is better than another argument.
- CSV and JSON get priority over other formats.
- Always think of scalability and memory issues. Favour streaming algorithms.
- DRY.

List of tools
-------------

`pdf`. Compute pdf


Examples
--------

Compute pdf of column 3 of a CSV file:

```
cat data.csv | col 3 pdfpi
```
