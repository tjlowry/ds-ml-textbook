# Functions

## Overview

The course was literally called "Programming with Functions," and the thesis was simple:
**every distinct task gets its own function, and the most reusable functions take parameters
and return a result** — they don't read `input()` or `print()`. That one rule is why the rest
of my code got testable and readable. STAT 624's Week 10 lecture layered on the computer-science
vocabulary — scope, DRY, `lambda`/`map`, time complexity — which I paraphrase here; the code is
my own CSE 111 work.

## How I did it — a pure-function library

The cleanest example is a physics assignment: a set of small **pure functions** that each take
numbers and return a number, with no I/O anywhere. That's the ideal shape — each one does a
single calculation and can be tested in isolation.

```python
def water_column_height(tower_height, tank_height):
    return tower_height + (3 * tank_height / 4)

def pressure_gain_from_water_height(height):
    density_water = 998.2
    acceleration_gravity = 9.80665
    return (density_water * acceleration_gravity * height) / 1000

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    density_water = 998.2
    return (-friction_factor * pipe_length * density_water * fluid_velocity**2) \
        / (2000 * pipe_diameter)
```

Then a single `main()` reads the user input, calls these in sequence, and prints — the input
and output live in *one* function, and all the actual math lives in reusable, testable ones.
That separation is exactly what makes the [testing](testing-with-pytest.md) page possible: I
can `assert pressure_gain_from_water_height(...) == expected` without ever prompting a user.

*Source: `course-files/11-python-programming/python_assignments/functions/functions_physics_formulas.py`
(my own code).*

## How I did it — a helper function inside a loop

A compound-interest assignment shows the smallest useful pattern: a `for` loop that calls a
helper each iteration. The helper is a one-liner, but pulling it out means the loop reads as
"for each year, get the future value" instead of burying the formula inline.

```python
def get_future_value(amount, monthly_rate, years):
    return amount * (1 + monthly_rate) ** (years * 12)

def main():
    amount = float(input("Please enter the amount: "))
    annual_rate = float(input("Please enter the annual rate: "))
    monthly = annual_rate / 1200
    for year in range(1, 31):
        value = get_future_value(amount, monthly, year)
        print(f"{year} - ${value:.2f}")

main()
```

*Source: `course-files/11-python-programming/python_assignments/loops/for_loop_compound_interest.py`
(my own code).*

## Pass-by-value vs pass-by-reference

The single most confusing thing about Python arguments — and I wrote an assignment purely to
pin it down. **Immutable objects (ints, strings, tuples) act pass-by-value; mutable objects
(lists, dicts) act pass-by-reference.** Rebinding a name inside a function is local; *mutating*
a mutable object reaches back out.

```python
def modify_args(n, alist):
    n += 1              # rebinds the local name -> caller's int is untouched
    alist.append(4)     # mutates the actual list -> caller sees the change

x = 5
lx = [7, -2]
modify_args(x, lx)
print(x, lx)            # -> 5 [7, -2, 4]
```

`x` comes back as `5` because `n += 1` just points the local `n` at a new integer. `lx` comes
back with a `4` appended because `alist` and `lx` are the *same list object* — `.append()`
mutates it in place. Once this clicked, a whole category of "why did my list change?" bugs
disappeared.

*Source: `course-files/11-python-programming/python_assignments/functions/pass_by_value_vs_reference.py`
(my own code).*

## DRY, and the refactor that sold me on functions

The end-of-course reflection asked where I saw the power of functions, and my honest answer was
my final project. I'd written a machine-learning program *before* without functions, and for
CSE 111 I rewrote the same thing — an NBA win-rate predictor — with the work split into
single-task functions:

```python
def load_dataset(): ...
def prepare_data(df): ...
def filter_dataset(df, team, season): ...
def perform_random_forest_classification(X, y): ...
def calculate_actual_winning_percentage(filtered_df): ...

def main():
    df = prepare_data(load_dataset())
    suns = filter_dataset(df, "PHO", 2022)
    X, y = suns[feature_cols], suns["won"]
    y_test, y_pred, accuracy = perform_random_forest_classification(X, y)
    ...
```

Same model, same ~75% accuracy — but the functioned version was *"so much cleaner and easier to
understand,"* to quote my own write-up. Each function had one job, so I could reason about (and
test) one at a time instead of holding the whole script in my head. This is the same
**"split the pipeline into stages"** instinct that the production forecasting work in the
[Time Series](../09-time-series-forecasting/index.md) chapter is built on, just in miniature —
`load → prepare → filter → model → evaluate` is a pipeline whether it's six functions or six
modules. **DRY** ("Don't Repeat Yourself") is the same idea from the other direction: when the
same lines show up twice, that's a function waiting to be named.

*Source: `course-files/11-python-programming/python_assignments/data_science/ml_random_forest.py`
and `.../reflection.txt` (my own code and reflection; the 12.6 MB dataset stays out of the
repo, so this is prose, not a runnable snippet).*

## Scope, `lambda`, and `map`

- **Scope.** A name assigned inside a function is local to it; to reassign a name from an outer
  scope you need `global` (module level) or `nonlocal` (enclosing function). In practice I
  avoid both — passing values in as parameters and returning results out is cleaner than
  reaching across scopes.
- **`lambda`.** A one-expression anonymous function, most useful as a `key=`: `sorted(rows,
  key=lambda r: r[2])` sorts by the third column. I use it exactly where the
  [data structures](data-structures.md#how-i-did-it-parallel-lists-and-sorting-with-a-key)
  page uses `itemgetter`.
- **`map`.** `map(f, xs)` applies `f` to every element lazily. A list comprehension
  `[f(x) for x in xs]` does the same thing and I find it clearer, but `map` is worth
  recognizing.

## Gotchas

- **Reusable = no I/O.** A function that calls `input()`/`print()` is hard to reuse and nearly
  impossible to test. Keep the math in parameter-in/result-out functions and confine I/O to
  `main()`.
- **Mutable default arguments.** `def f(items=[]):` reuses the *same* list across every call —
  a classic footgun. Use `def f(items=None): items = items or []`.
- **Rebinding isn't mutating.** `n += 1` on an int inside a function doesn't touch the caller;
  `alist.append(x)` on a list does. Know which one you're doing.

## References

- STAT 624 Week 10 — Functions (local:
  `course-files/11-python-programming/Week10_Function.ipynb`). Instructor material, © 2023
  Scott A. Bruce, do-not-distribute; concept summary only.
