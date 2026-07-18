# Testing with pytest

## Overview

CSE 111 drilled one habit hard: write **test functions** for your pure functions. In my own
end-of-course reflection I put it plainly — test functions are valuable because they *confirm
the result your function produces* and let you check it against known inputs in a controlled
setting, instead of eyeballing the program's output and hoping. That's the entire case for
automated testing in one sentence, and it's why every function-heavy chapter downstream leans
on tests.

**pytest** is the tool: you write functions named `test_*`, put `assert` statements inside
them, and pytest discovers and runs them, reporting exactly which assertion failed and with
what values.

## How I did it — testing a pure function

The [physics-formula library](functions.md#how-i-did-it-a-pure-function-library) is the ideal
thing to test: each function takes numbers and returns a number, no I/O. A test just calls it
with known inputs and asserts the expected output. Because the outputs are floats, I compare
with `pytest.approx` rather than `==` — floating-point arithmetic rarely lands on an exact
decimal:

```python
import pytest
from water_flow import (
    water_column_height,
    pressure_gain_from_water_height,
)

def test_water_column_height():
    # Two cases, so a single wrong constant can't pass by luck.
    assert water_column_height(0, 0) == 0
    assert water_column_height(10, 20) == pytest.approx(25.0)   # 10 + 3*20/4

def test_pressure_gain_from_water_height():
    assert pressure_gain_from_water_height(0) == 0
    # 998.2 * 9.80665 * 30 / 1000
    assert pressure_gain_from_water_height(30) == pytest.approx(293.71, abs=0.01)
```

Run it with `pytest`, and a green dot per test means the math still holds; a failure prints the
actual vs expected values right at the assertion. Two things I'm deliberate about:

- **More than one assertion per function.** A single test case can pass by coincidence (a
  formula off by a constant might still return the right number for one input). Two or three
  cases pin the behavior down.
- **`pytest.approx` for floats.** `assert 0.1 + 0.2 == 0.3` is `False` in Python. `approx`
  compares within a tolerance, which is what you almost always want for computed floats.

*The test above is written fresh for this page. My actual CSE 111 test files followed this
pattern but several started from instructor-provided grading harnesses, so I don't reproduce
them — see the honest note below.*

## How I did it — testing the ML project's helpers

My final-project write-up lists the test functions I wrote for the NBA win-rate predictor —
`test_prepare_data`, `test_filter_dataset`, `test_calculate_actual_winning_percentage`,
`test_calculate_predicted_winning_percentage` — each with two example cases. The point of
[splitting that project into single-task functions](functions.md#dry-and-the-refactor-that-sold-me-on-functions)
was precisely that it made them testable: `calculate_predicted_winning_percentage(wins, games)`
is a pure ratio I can assert on, whereas the `main()` that prints results is not. That's the
testing payoff of the whole "keep I/O out of your logic" rule.

*Source: `course-files/11-python-programming/python_assignments/data_science/explination.txt`
and `.../reflection.txt` (my own project write-up and reflection).*

## An honest note: the test files don't run as committed

Worth recording as a real gotcha. My CSE 111 `testing/` folder has nine `pytest_*.py` files,
and **none of them run standalone as checked out** — each imports a sibling implementation
module (`water_flow`, `chemistry`, `formula`, etc.) that isn't present under that exact
filename in the same folder. The folder was clearly assembled by pulling test files away from
the implementation files they were paired with. So the tests are correct *patterns*, but a bare
`pytest` in that directory fails at import, not at assertion. It's the reason the notebook for
this chapter re-pairs two of my files by hand (the periodic-table dict and the formula parser)
so it can actually execute — see the
[chemical-formula-parser notebook](notebooks/chemical-formula-parser.ipynb), which ends with a
few inline `assert` checks in exactly this spirit.

## Gotchas

- **Name tests `test_*`.** pytest discovers functions by that prefix; a mis-named test is
  silently never run, which looks identical to "all tests pass."
- **Never `==` two floats.** Use `pytest.approx` (or `math.isclose`). Exact float equality is a
  flaky-test generator.
- **A test that imports a missing module fails at collection, not assertion.** If `pytest`
  reports errors before any test runs, it's usually an import problem — check that the code
  under test is actually importable from where you run pytest. (This is exactly what bit my
  `testing/` folder.)
- **One assertion is not a test.** Pin behavior with a couple of cases so a coincidentally-right
  output can't turn the bar green.

## References

- STAT 624 Week 10 — Functions (testing motivation) (local:
  `course-files/11-python-programming/Week10_Function.ipynb`). Instructor material, © 2023
  Scott A. Bruce, do-not-distribute; concept summary only.
