# NumPy Arrays

## Summary

pandas is built on NumPy. A DataFrame column is a NumPy array with a label, and most of the
speed and vectorized behavior you get from pandas is really NumPy underneath. So a page on
data wrangling needs a page on the array — what makes `np.ndarray` different from a Python
list, why *vectorized* operations are both faster and clearer than loops, and how
**broadcasting** lets arrays of different shapes combine without writing any loop at all.

> **Source note.** The material on this page is one I first learned from the Texas A&M
> **STAT 624 ("Computing Tools for Data Science," Prof. Scott A. Bruce)** "Week 12" NumPy &
> pandas notebook (local: `course-files/04-data-wrangling/Week 12. NumPy and pandas.ipynb`).
> That notebook is the instructor's copyrighted, do-not-distribute material, so **nothing
> here is copied from it** — every example below is written from scratch. It's cited as the
> place I picked up the concepts, nothing more.

## Arrays vs. lists

A Python list is a container of arbitrary objects, each a full Python object with its own
type. A NumPy array is a single block of one fixed numeric type (`dtype`) laid out
contiguously in memory. That difference is the whole story: because every element is the same
type and packed together, NumPy can push arithmetic down into compiled C loops instead of
interpreting Python bytecode per element.

```python
import numpy as np

nums = [1, 2, 3, 4]        # Python list of int objects
arr = np.array([1, 2, 3, 4])   # ndarray, dtype=int64, one memory block

arr.dtype    # dtype('int64')
arr.shape    # (4,)
arr * 2      # array([2, 4, 6, 8])  -- elementwise, no loop
```

Note `arr * 2` multiplies every element, while `nums * 2` on the list would *repeat* it
(`[1, 2, 3, 4, 1, 2, 3, 4]`). The array overloads arithmetic to mean "apply to each element,"
which is exactly what you want on a column of data.

## Vectorization

**Vectorization** means expressing an operation on a whole array at once instead of looping
element by element. Beyond being faster, it's usually *shorter and clearer* — the code says
what you mean ("normalize this array") rather than how to iterate it.

```python
# Looped: explicit, slow, noisy
out = np.empty_like(arr, dtype=float)
for i in range(len(arr)):
    out[i] = (arr[i] - arr.mean()) / arr.std()

# Vectorized: one line, and NumPy runs the loop in C
out = (arr - arr.mean()) / arr.std()
```

The speed gap is real and grows with size. A quick timing of squaring a million numbers, a
list comprehension versus a vectorized array op:

```python
import numpy as np, time

n = 1_000_000
py = list(range(n))
npy = np.arange(n)

t = time.perf_counter(); _ = [x * x for x in py]; print("list:", time.perf_counter() - t)
t = time.perf_counter(); _ = npy * npy;           print("numpy:", time.perf_counter() - t)
# numpy is typically ~50-100x faster here
```

The habit to build: if you find yourself writing a `for` loop over a DataFrame column or an
array, stop and ask whether a vectorized expression (or `.apply`, or a boolean mask) does the
same thing. It almost always does.

## Broadcasting

**Broadcasting** is the rule that lets NumPy combine arrays of different shapes by virtually
stretching the smaller one to match — again with no loop and no copied data. The simplest
case is array-with-scalar (`arr * 2` above); the general rule aligns shapes from the trailing
dimension, and dimensions of size 1 stretch to fit.

```python
# (3, 3) matrix minus a (3,) row vector -> the vector is broadcast down every row
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
col_means = X.mean(axis=0)      # shape (3,) -> [4., 5., 6.]
centered = X - col_means        # each column has its mean subtracted, no loop
```

That last line is exactly how you mean-center features before something like PCA — a real
wrangling/preprocessing step, done in one broadcast expression. Broadcasting is why NumPy
code that operates on rows, columns, or whole matrices stays compact.

## Why this sits under pandas

When you write `df['x'] - df['x'].mean()`, or filter with `df[df['x'] > 0]`, or call
`df['x'].values`, you are using NumPy: the column is an ndarray, the comparison is vectorized,
the boolean mask is a NumPy array. Understanding the array makes the DataFrame's behavior —
its speed, its broadcasting, its dtype rules — stop being magic. The
[pandas fundamentals](pandas-fundamentals.md) page's dtype gotcha (one text value forcing a
whole column to `object`) is really a NumPy fact: an array holds exactly one dtype, and mixing
types drops you to the `object` dtype where the C fast-path no longer applies.

## Gotchas

- **NumPy arithmetic can silently overflow.** A fixed integer dtype (`int32`, `int64`) wraps
  around on overflow instead of promoting to a bigger type the way Python ints do. Watch it
  when summing large counts; cast to `float64` or a wider int if in doubt.
- **Integer arrays can't hold `NaN`.** `NaN` is a float. The moment a column has a missing
  value it becomes float (or `object`), which is one reason pandas often shows integer-looking
  columns as floats after a merge or a `replace`.
- **Broadcasting fails loudly only when shapes truly don't align.** A `(3,)` vector will
  broadcast against a `(3, 3)` matrix, but so will a `(1, 3)` — and if you meant it as a
  column you'll get a silently wrong result rather than an error. Check shapes with `.shape`
  when a broadcast result looks off.
- **A NumPy slice is a *view*, not a copy.** Modifying `arr[2:5]` mutates the original array.
  Use `.copy()` when you need an independent piece — the same trap exists in pandas as the
  `SettingWithCopyWarning`.
