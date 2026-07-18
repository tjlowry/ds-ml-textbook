# Classes & OOP

## Overview

A **class** is a template for an object that bundles data (attributes) with the functions that
operate on it (methods). Where a [function](functions.md) is a verb, a class is a noun that
knows how to do things to itself. STAT 624's Week 10 classes lecture walked through `__init__`,
`self`, the different method kinds, and `@property`; I paraphrase those concepts here and pair
them with the one piece of real class code from my CSE 111 work — a custom exception — plus a
short tkinter aside.

## The anatomy of a class

```python
class Molecule:
    """A named molecule with a chemical formula."""

    # Class attribute: shared by every instance.
    AVOGADRO = 6.02214076e23

    def __init__(self, name, formula):
        # Instance attributes: unique to each object, set on construction.
        self.name = name
        self.formula = formula
        self._molar_mass = None      # a leading underscore = "internal, don't poke"

    def describe(self):
        """An instance method: takes self, acts on this object's data."""
        return f"{self.name} ({self.formula})"

    @property
    def molar_mass(self):
        """A property: called like an attribute (m.molar_mass), computed on demand."""
        if self._molar_mass is None:
            self._molar_mass = self._compute_mass()
        return self._molar_mass

    @staticmethod
    def is_valid_symbol(symbol):
        """A static method: related to the class but needs no instance."""
        return symbol.isalpha() and symbol[0].isupper()

water = Molecule("Water", "H2O")
print(water.describe())          # Water (H2O)
print(Molecule.is_valid_symbol("O"))   # True
```

The pieces, in the order they trip people up:

- **`__init__` and `self`.** `__init__` is the constructor — it runs when you call
  `Molecule(...)`. `self` is the instance being built; `self.name = name` stores a value *on
  that object*. Every instance method takes `self` as its first parameter, and Python passes it
  automatically when you write `water.describe()`.
- **Instance vs class attributes.** `self.name` is per-object; `AVOGADRO` is defined on the
  class and shared by all instances. Reach for a class attribute for genuine constants only.
- **Instance / static / class methods.** An instance method needs the object's data (`self`).
  A `@staticmethod` is just a plain function that lives in the class's namespace because it's
  topically related. (A `@classmethod`, which I use less, takes the class itself as `cls` —
  handy for alternate constructors.)
- **`@property`.** Lets `water.molar_mass` *look* like a plain attribute while actually running
  a method — so I can compute it lazily and cache it, and callers never know the difference.
  It's the Pythonic answer to Java-style `getMolarMass()`.

*The `Molecule` sketch above is a fresh illustration written for this page. The STAT 624 class
lecture is instructor-copyrighted, so I don't reproduce its examples.*

## How I did it — a custom exception class (the real thing)

The one place I wrote a genuine class in CSE 111 was defining my *own* exception type. A
custom exception is the smallest useful class: it inherits from a built-in exception and
usually adds nothing but a name — but that name is the point. Now callers can catch *my* error
specifically instead of a generic `ValueError`.

```python
class FormulaError(ValueError):
    """The error raised when parse_formula gets an invalid chemical formula."""


def parse_formula(formula, periodic_table_dict):
    ...
    if symbol not in periodic_table_dict:
        raise FormulaError(f"invalid formula; unknown element symbol: {symbol}",
                           formula, index)
    ...
```

Because `FormulaError` subclasses `ValueError`, calling code can catch it two ways: precisely
(`except FormulaError`) when it wants to react to a bad formula specifically, or broadly
(`except ValueError`) when any value problem is handled the same way. That inheritance
relationship is the whole reason to define the class — it's a worked example of the
[inheritance](inheritance.md) page's idea and the [error handling](error-handling.md) page's
`raise`. The full parser is executed end-to-end in the
[chemical-formula-parser notebook](notebooks/chemical-formula-parser.ipynb).

*Source: `course-files/11-python-programming/python_assignments/classes/classes_custom_exception.py`
(my own code).*

## Aside: classes behind a tkinter GUI

CSE 111 also had me build a small **tkinter** desktop GUI — a "heart rate" calculator with
labels, entry boxes, and a button. The lesson there was that a GUI is *classes all the way
down*: the framework hands you widget classes (`Label`, `Entry`, `Button`), and the natural way
to organize the app is to subclass `Entry` into a custom `IntEntry`/`FloatEntry` that validates
its own input. The skeleton for those widget subclasses was instructor-provided, so I won't
reproduce it, but the shape of a minimal tkinter app is worth remembering:

```python
import tkinter as tk

class HeartRateApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)          # initialize the parent Frame
        self.pack()
        tk.Label(self, text="Age:").pack()
        self.age = tk.Entry(self)
        self.age.pack()
        tk.Button(self, text="Compute", command=self.compute).pack()

    def compute(self):
        age = int(self.age.get())
        print(f"Max heart rate ≈ {220 - age}")

root = tk.Tk()
HeartRateApp(root)
root.mainloop()
```

The `super().__init__(master)` call is the same `super()` I lean on in the
[inheritance](inheritance.md) page. GUI work is a small corner of my Python — this aside is as
deep as this book goes on it.

*Concept from `course-files/11-python-programming/python_assignments/gui/` (my own UI wiring;
the widget-subclass module was instructor-templated and is not reproduced). The snippet above
is a fresh minimal example.*

## Gotchas

- **Forgetting `self`.** Every instance method's first parameter is `self`, and every access to
  the object's own data goes through it — `self.name`, not `name`. Leaving it off is the most
  common beginner error.
- **Mutable class attributes are shared.** A list defined at class level (`items = []`) is one
  list shared by *all* instances. Per-object state belongs in `__init__` as `self.items = []`.
- **A property that does real work is a trap.** `@property` makes a method look like a cheap
  attribute access. Keep the computation light (or cache it, as `molar_mass` does) — callers
  won't expect `obj.x` to be expensive.

## References

- STAT 624 Week 10 — Classes (local:
  `course-files/11-python-programming/Week10_classes.ipynb`). Instructor material, © 2023
  Scott A. Bruce, do-not-distribute; concept summary only.
