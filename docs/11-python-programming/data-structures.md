# Data Structures

## Overview

Python gives you four built-in collections, and picking the right one is most of the battle:

- **list** — ordered, mutable, indexable. The default when order matters or you'll append.
- **dict** — key → value mapping with O(1) lookup. The default when you'll look things up
  *by* something other than position.
- **tuple** — an immutable, fixed-length record. A row of data that shouldn't change.
- **set** — an unordered collection of unique elements. Membership tests and dedup.

STAT 624's Week 9 lecture framed the whole thing as "choosing the right structure," and that
framing stuck with me more than any single method name. The concepts below are paraphrased
from that lecture; the code is from my own CSE 111 assignments.

## How I did it — a dict of lists (the periodic table)

My favorite CSE 111 use of a dictionary was a periodic table, where each **key** is an element
symbol and each **value** is a small list holding the element's name and atomic mass. That
"dict whose values are lists" shape shows up constantly — it's a lightweight record store
before you reach for a class.

```python
def make_periodic_table():
    periodic_table_dict = {
        "H":  ["Hydrogen", 1.00794],
        "He": ["Helium",   4.002602],
        "C":  ["Carbon",   12.0107],
        "O":  ["Oxygen",   15.9994],
        "Fe": ["Iron",     55.845],
        # ... 90-odd more elements
    }
    return periodic_table_dict

# Named indexes beat magic numbers for the inner lists.
NAME_INDEX = 0
ATOMIC_MASS_INDEX = 1

table = make_periodic_table()
mass_of_oxygen = table["O"][ATOMIC_MASS_INDEX]   # 15.9994
```

The lookup is the point: `table["O"]` is instant regardless of how many elements are in the
dict, whereas finding oxygen in a *list* of elements would mean scanning until I hit it. The
`NAME_INDEX` / `ATOMIC_MASS_INDEX` constants are a small habit I picked up in this course —
`table["O"][1]` works but `table["O"][ATOMIC_MASS_INDEX]` says what it means.

*Source: `course-files/11-python-programming/python_assignments/dictionaries/dictionaries_periodic_table.py`
(my own code). The full table plus the parser that consumes it is executed in the
[chemical-formula-parser notebook](notebooks/chemical-formula-parser.ipynb).*

## How I did it — parallel lists and sorting with a key

Another assignment loaded a CSV of records into a **compound list** (a list of rows, each row
itself a list) and sorted it different ways. The lesson was that `sorted()` takes a `key`
function that says *what to sort by* — so the same list can be ordered by any field without
touching the data:

```python
from operator import itemgetter

# Each row is [given_name, surname, birthdate]; column positions as constants.
GIVEN_NAME_INDEX = 0
BIRTHDATE_INDEX = 2

# Sort oldest-to-youngest by the birthdate column...
by_birthdate = sorted(records, key=itemgetter(BIRTHDATE_INDEX))

# ...or alphabetically by given name, from the same list.
by_name = sorted(records, key=itemgetter(GIVEN_NAME_INDEX))
```

`itemgetter(2)` builds a function that pulls element `2` out of each row — the same thing as
`lambda row: row[2]`, just faster and more readable. This is the bridge to the
[Functions](functions.md#scope-lambda-and-map) page, where `lambda` and `key=` come back.

*Source: `course-files/11-python-programming/python_assignments/lists/lists_sorting_lambda.py`
(my own code; the original loaded a roster fixture that held real names, so the rows above are
illustrative).*

## Tuples and sets, briefly

- **Tuple** — I reach for a tuple when a group of values belongs together and shouldn't be
  reassigned: `("Widget", 3, 4.99)` for a receipt line item. Because it's immutable it can
  also be a dict key or live in a set, which a list can't.
- **Set** — `set(symbols)` drops duplicates instantly, and `"O" in seen` is an O(1) membership
  test. When I catch myself writing `if x not in already_seen_list`, that's the signal a set
  was the right structure.

## Gotchas

- **Dict lookup vs list scan.** The whole reason to use a dict is the O(1) lookup. If you find
  yourself looping through a list to find a matching field, you probably wanted a dict keyed on
  that field (exactly the [File I/O](file-io.md) `read_dictionary` pattern).
- **Mutable default trap.** Lists and dicts are mutable, so passing one into a function lets
  the function change it in place — see [pass-by-reference](functions.md#pass-by-value-vs-pass-by-reference).
  Never use a mutable object as a function's default argument.
- **Name your indexes.** `row[2]` three functions deep is a bug waiting to happen. A
  `BIRTHDATE_INDEX = 2` constant costs one line and saves the "wait, which column was that?"
  every time.

## References

- STAT 624 Week 9 — Python data structures (local:
  `course-files/11-python-programming/Week9_python_datastructures.ipynb`). Instructor
  material, © 2023 Scott A. Bruce, do-not-distribute; concept summary only.
