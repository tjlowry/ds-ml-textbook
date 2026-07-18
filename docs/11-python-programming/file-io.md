# File I/O

## Overview

Most of my CSE 111 programs read a CSV, did something with it, and sometimes wrote a result
back out. Two patterns cover nearly all of it: **the `with open(...)` context manager** for
safe file handling, and **loading a CSV into a dictionary keyed on one column** for fast
lookups. Both are my own code below.

## How I did it — the read-into-a-dict pattern

The most reused function across my assignments read a CSV into a dictionary, using one column
as the key so later code could look rows up in O(1) instead of scanning:

```python
import csv

def read_dictionary(filename, key_column_index):
    """Read a CSV into a dict keyed on key_column_index; each value is the full row."""
    dictionary = {}
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)                       # skip the header row
        for row_list in reader:
            if len(row_list) != 0:
                key = row_list[key_column_index]
                dictionary[key] = row_list
    return dictionary

products = read_dictionary("products.csv", 0)   # key on the product-ID column
name  = products["A100"][1]
price = float(products["A100"][2])
```

The pieces worth calling out:

- **`with open(...) as f:`** — the context manager. The file is guaranteed to close when the
  block exits, even if an exception fires mid-read. I never call `open()` without `with`.
- **`csv.reader` + `next(reader)`** — `csv.reader` yields one list per row and handles quoting/
  commas for me; `next(reader)` throws away the header line before the loop.
- **Keying the dict** — turning the file into `{"A100": ["A100", "Widget", "4.99"], ...}` means
  the receipt code that consumes it does `products[id]` instead of looping to find the match.
  That's the [data structures](data-structures.md#gotchas) "dict beats a list scan" lesson in
  practice, and the `KeyError` it can raise is exactly what the
  [error handling](error-handling.md#how-i-did-it-tryexcept-around-a-dict-lookup) page guards.

*Source: `course-files/11-python-programming/python_assignments/file_io/` and
`.../error_handling/try_except_receipt.py` (my own code; the fixture is the invented
`products.csv` grocery list — never the roster fixture that held real student IDs).*

## How I did it — writing to a file

A tire-shop assignment computed the air volume inside a tire and *appended* a timestamped line
to a running log file. Writing is the same `with open(...)` context manager, opened in append
mode (`"at"`) so each run adds a line instead of clobbering the file:

```python
import math
from datetime import datetime

width = float(input("Tire width in mm: "))
aspect_ratio = float(input("Aspect ratio: "))
diameter = float(input("Wheel diameter in inches: "))

volume_cc = math.pi * (width ** 2) * aspect_ratio \
    * (width * aspect_ratio + 2540 * diameter) / 10_000_000
volume_l = volume_cc / 1000

with open("volumes.txt", "at") as log_file:
    print(datetime.now(), width, aspect_ratio, diameter, volume_l, file=log_file)

print(f"The approximate volume of air inside the tire is {volume_l:.1f} liters.")
```

The trick I like here is `print(..., file=log_file)` — the same `print` I use for the console,
just redirected to the file, so formatting is one familiar call instead of manual
`log_file.write(...)` string-building. The mode string is the whole difference between
behaviors: `"rt"` read, `"wt"` overwrite, `"at"` append.

*Source: `course-files/11-python-programming/python_assignments/file_io/file_write_tire_log.py`
(my own code).*

## Gotchas

- **Always use `with`.** Manually `open()`/`close()` leaks file handles the moment an exception
  jumps over your `close()`. The context manager closes the file no matter how the block exits.
- **`"w"` truncates immediately.** Opening in write mode empties the file before you write a
  byte — one wrong mode letter and the previous contents are gone. Use `"a"` to append.
- **Skip the header, or parse it as data by accident.** Forgetting `next(reader)` silently
  loads the column-name row as if it were a record — a bug that surfaces far downstream.
- **CSV cells are strings.** `csv.reader` gives you strings; `float(row[2])` / `int(row[1])`
  conversions are on you, and they're the `ValueError` the
  [error handling](error-handling.md) page catches.

## References

- STAT 624 Week 9 — Python data structures (file/CSV concepts) (local:
  `course-files/11-python-programming/Week9_python_datastructures.ipynb`). Instructor material,
  © 2023 Scott A. Bruce, do-not-distribute; concept summary only.
