# Error Handling

## Overview

Real programs meet bad input: a missing file, a non-numeric value where a number was expected,
a lookup key that isn't there. Python's answer is `try`/`except` — attempt the risky code, and
if it raises, catch the specific exception and recover instead of crashing. The rule I learned
in CSE 111: **catch the narrowest exception that fits, and let everything else propagate.** A
bare `except:` that swallows all errors hides the bug you actually need to see.

## How I did it — catching several specific exceptions

A traffic-safety assignment read a national accident-statistics CSV (public aggregate data —
no personal information) and computed hypothetical injury reductions. File reading and number
parsing are both fallible, so the whole thing runs under a `try` with one `except` per failure
mode:

```python
import csv

def main():
    try:
        filename = input("Name of file that contains NHTSA data: ")
        with open(filename, "rt") as text_file:
            perc_reduc = float(input("Percent reduction [0, 100]: "))
            reader = csv.reader(text_file)
            next(reader)                      # skip the header row
            for row in reader:
                injuries, deaths = estimate_reduction(row, PHONE_COLUMN, perc_reduc)
                print(row[YEAR_COLUMN], injuries, deaths, sep=", ")

    except FileNotFoundError as err:
        print(f"error: {err}")
    except (PermissionError, csv.Error) as err:
        print(f"error: {err}")
    except ValueError as err:                 # float("abc") raises this
        print(f"error: {err}")
```

Three things I do deliberately here:

- **One `except` per failure mode.** `FileNotFoundError` (bad filename), `PermissionError`/
  `csv.Error` (can't read it), and `ValueError` (`float()` on non-numeric input) each get their
  own handler, so the message tells the user what actually went wrong.
- **Group related exceptions in a tuple.** `except (PermissionError, csv.Error)` handles two
  types the same way without duplicating the block.
- **Catch specific types, in order.** Python tries the `except` clauses top-to-bottom and takes
  the first match, so narrower exceptions go first.

*Source: `course-files/11-python-programming/python_assignments/error_handling/try_except_multiple.py`
(my own code; `accidents.csv` is public-style aggregate national data).*

## How I did it — try/except around a dict lookup

A receipt-builder read a products file into a dictionary and looked up each requested item. A
missing product ID raises `KeyError`, so I guard the lookup and fail with a message that names
the offending ID rather than dumping a traceback:

```python
try:
    product_info = products_dict[product_num]
except KeyError:
    print(f"Error: unknown product ID '{product_num}' in the request file")
    return
```

This is the everyday use of `try`/`except`: not exotic recovery, just turning a crash into a
clear message. It pairs directly with the [File I/O](file-io.md) `read_dictionary` pattern.

*Source: `course-files/11-python-programming/python_assignments/error_handling/try_except_receipt.py`
(my own code; uses the invented `products.csv` grocery fixture).*

## Raising your own exceptions

The other half of error handling is *raising*. When my chemical-formula parser hits an unknown
element symbol, it doesn't return a sentinel value — it raises the custom
[`FormulaError`](classes-and-oop.md#how-i-did-it-a-custom-exception-class-the-real-thing) so
the caller can decide how to handle it:

```python
if symbol not in periodic_table_dict:
    raise FormulaError(f"invalid formula; unknown element symbol: {symbol}",
                       formula, index)
```

Because `FormulaError` subclasses `ValueError`, a caller can catch it precisely
(`except FormulaError`) or fold it into general value handling (`except ValueError`). Raising a
*specific* exception type — rather than a generic `Exception` — is what makes that choice
possible. The parser and a demo of this exception firing on a bad formula are executed in the
[chemical-formula-parser notebook](notebooks/chemical-formula-parser.ipynb).

## Gotchas

- **Never use a bare `except:`.** Catching everything hides real bugs (typos, `KeyboardInterrupt`,
  logic errors) behind a generic "something went wrong." Name the exception you expect.
- **Order matters.** Since Python takes the first matching clause, list specific exceptions
  before their base classes — a leading `except Exception` would shadow everything after it.
- **Don't catch what you can't handle.** If a function can't sensibly recover from an error,
  let it propagate to a caller that can. Catching just to re-raise or to print-and-continue
  past a real problem is worse than not catching at all.
- **`raise` beats returning a sentinel.** Returning `None` or `-1` on failure forces every
  caller to remember to check; raising makes the failure impossible to ignore silently.

## References

- STAT 624 Week 10 — Functions (error-handling concepts) (local:
  `course-files/11-python-programming/Week10_Function.ipynb`). Instructor material, © 2023
  Scott A. Bruce, do-not-distribute; concept summary only.
