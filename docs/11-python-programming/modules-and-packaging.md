# Modules & Packaging

## Overview

A **module** is just a `.py` file. The moment you write `import`, you're using the module
system — pulling in code from the standard library, a third-party package, or another file of
your own. STAT 624's Week 10 lecture covered running scripts from the command line, imports,
and shebangs; the concepts are paraphrased here, the code is my own CSE 111 work.

## How I did it — importing from the standard library

The smallest example is a tire-volume calculator that imports `math` for `pi` and does one
computation. Nothing exotic — but it's the everyday shape of "reach into the standard library
for the constant/function you need":

```python
import math

width = int(input("Enter the width of the tire in mm (ex 205): "))
aspect_ratio = int(input("Enter the aspect ratio of the tire (ex 60): "))
diameter = int(input("Enter the diameter of the wheel in inches (ex 15): "))

volume_cc = math.pi * (width ** 2) * aspect_ratio \
    * (width * aspect_ratio + 2540 * diameter) / 10_000_000
volume_l = volume_cc / 1000

print("The approximate volume is {:.2f} liters".format(volume_l))
```

`import math` binds the module to the name `math`, and `math.pi` reaches the constant inside
it. The `csv` and `datetime` imports on the [File I/O](file-io.md) page are the same mechanism
for bigger modules.

*Source: `course-files/11-python-programming/python_assignments/modules/math_module_tire_calc.py`
(my own code).*

## Script vs module, and `if __name__ == "__main__"`

The same `.py` file can be **run** as a script (`python myfile.py`) or **imported** by another
file. The guard that makes both work is one of the most important idioms in Python:

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

When a file is run directly, Python sets its `__name__` to `"__main__"`, so the `if` is true
and `main()` runs. When the same file is *imported*, `__name__` is the module's name instead,
the `if` is false, and `main()` does **not** run — the importer gets the functions without
triggering the script's side effects. This is exactly what makes the
[testing](testing-with-pytest.md) story possible: a test file can `import` my module to reach
its functions without kicking off a `main()` that prompts for input. Nearly every one of my
CSE 111 programs ends with this guard.

- **Import forms.** `import math` (whole module, `math.pi`), `from math import pi` (one name,
  bare `pi`), `from operator import itemgetter` (the form the
  [data structures](data-structures.md#how-i-did-it-parallel-lists-and-sorting-with-a-key) page
  uses). Prefer the explicit `import module` / `from module import name` forms over
  `from module import *`, which dumps unknown names into your namespace.
- **A shebang** (`#!/usr/bin/env python3` as the first line) lets a Unix shell run the file
  directly as `./myfile.py` once it's executable — a convenience for CLI scripts, not needed
  when you invoke `python myfile.py` yourself.

## From files to packages

Scaling up: a **package** is a directory of modules (historically marked by an `__init__.py`).
The production forecasting code in the [Time Series](../09-time-series-forecasting/index.md)
chapter is organized that way — `features/lag.py`, `evaluation/metrics.py`, and so on, imported
as `from features.lag import LagFeatureEngineer`. It's the same `import` machinery as
`import math`, just pointed at my own directory tree instead of the standard library. The CSE
111 assignments never got that big, but the mental model is identical: a file is a module, a
folder of modules is a package, and `import` is how they find each other.

## Gotchas

- **Top-level code runs on import.** Any statement not inside a function or the
  `if __name__ == "__main__"` guard executes the moment the module is imported. Put runnable
  entry-point code under the guard, or importing your file will trigger prompts and prints.
- **Avoid `from module import *`.** It hides where names come from and can silently shadow your
  own. Import the module, or the specific names you need.
- **Filename ≠ package name collisions.** Naming your own file `math.py` or `csv.py` can shadow
  the standard-library module of the same name on the import path — a genuinely confusing bug.
- **`__name__` is the whole trick.** If a script's `main()` runs when you only meant to import
  it, you forgot the `if __name__ == "__main__"` guard.

## References

- STAT 624 Week 10 — Functions (modules, imports, running scripts) (local:
  `course-files/11-python-programming/Week10_Function.ipynb`). Instructor material, © 2023
  Scott A. Bruce, do-not-distribute; concept summary only.
