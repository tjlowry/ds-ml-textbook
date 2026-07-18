# Missing Data: A Flights Case Study

## Summary

This is my DS 250 Project 2 — a single messy real-world dataset walked from raw file to clean
answers, where the whole challenge is **missing data done four different ways**. The dataset
is U.S. flight-delay counts by airport and month, and it's a good teaching case because it
mixes every missing-data problem at once: a numeric sentinel (`-999`), string sentinels
(blanks, `"NA"`, and the literal `"1500+"`), plain `NaN`, and — the interesting part — a
column that doesn't exist in the file at all and has to be *reconstructed from business
rules*.

The runnable version is the [flights notebook](notebooks/flights-data-wrangling.ipynb); this
page pulls out the wrangling decisions. All snippets come from
`~/Projects/school/byui-undergrad/DS_250/Project 2/Project2.qmd` (my own, DS 250; mirrored and
re-run at `course-files/04-data-wrangling/flights_data_wrangling.ipynb`). The assignment
prompts are the instructor's; I paraphrase them.

> **Data.** The public
> [byuidatascience `flights_missing`](https://github.com/byuidatascience/data4missing)
> dataset, loaded straight from its GitHub raw URL — I don't re-host it. The notebook fetches
> it at runtime.

## Step 1 — the numeric sentinel

Two columns use `-999` to mean "missing." Left alone, that's a catastrophe: `-999` is a
perfectly valid number to pandas, so any mean or sum over those columns is dragged wildly
negative and no `.isna()` check ever flags it. So the very first thing, before any analysis,
is mapping `-999` to a real `NaN`:

```python
def replace_negative_with_nan(df, column_names):
    df[column_names] = df[column_names].replace(-999, np.nan)
    return df

columns_to_replace = ['minutes_delayed_nas', 'num_of_delays_late_aircraft']
df = replace_negative_with_nan(df, columns_to_replace)
```

## Step 2 — aggregate to answer "worst airport"

*(Paraphrased task: pick a metric for the "worst" airport, then build a per-airport summary
table of total flights, delayed flights, proportion delayed, and average delay in hours.)*

This is a `groupby` + derived-column exercise. I aggregate each raw count to the airport
level, then compute the two metrics I care about — how *often* a delay happens and how *long*
it lasts:

```python
total_flights = df.groupby('airport_code')['num_of_flights_total'].sum()
total_delays = df.groupby('airport_code')['num_of_delays_total'].sum()
total_delay_minutes = df.groupby('airport_code')['minutes_delayed_total'].sum()

average_delay_hours = (total_delay_minutes / total_delays / 60).round(2)
proportion_delayed = (total_delays / total_flights).round(2)

summary_table = pd.DataFrame({
    'Total Flights': total_flights,
    'Total Delays': total_delays,
    'Proportion of Delayed Flights': proportion_delayed,
    'Average Delay (hours)': average_delay_hours,
})
```

I read Orlando as the worst — ~26% of flights delayed and the longest average delay at 1.13
hours. Using proportion *and* average length together avoids being fooled by a busy airport
with many but short delays.

## Step 3 — drop rows missing the grouping key

*(Paraphrased task: find the best month to fly, charting proportion delayed by month with the
x-axis in calendar order.)*

Before grouping by month, rows with a missing `month` have to go — you can't bucket an
observation by a key it doesn't have. `dropna(subset=...)` targets exactly that column:

```python
df = df.dropna(subset=['month'])
```

Then it's the same `groupby` pattern as Step 2, plus one wrangling detail worth calling out:
months are *ordinal*, not alphabetical, so I make `Month` an ordered categorical before
sorting, otherwise the x-axis comes out April-August-December:

```python
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
results['Month'] = pd.Categorical(results['Month'], categories=month_order, ordered=True)
results = results.sort_values('Month')
```

## Step 4 — reconstruct a column from business rules

*(Paraphrased task: build a new "total weather delay" column. The raw "Weather" category only
counts severe weather; mild-weather delays are hidden inside the NAS and Late-Arriving-Aircraft
categories. Fill missing Late-Aircraft values with the column mean, then apply three rules:
100% of Weather-category delays count; 30% of Late-Aircraft delays count; and NAS delays count
40% from April–August, 65% otherwise.)*

This is the most wrangling-heavy step, and the most realistic: **the column you need does not
exist in the data.** It's defined by domain rules, and building it means (a) imputing a gap
first, then (b) an `apply` that runs the rules row by row because one rule depends on the
month:

```python
# Impute the Late-Aircraft gaps with the column mean before applying the rules.
df['num_of_delays_late_aircraft'] = df['num_of_delays_late_aircraft'].fillna(
    df['num_of_delays_late_aircraft'].mean())

def calculate_weather_delay(row):
    if row['month'] in ['April', 'May', 'June', 'July', 'August']:
        nas_delay = round(0.4 * row['num_of_delays_nas'])
    else:
        nas_delay = round(0.65 * row['num_of_delays_nas'])
    weather_delay = row['num_of_delays_weather']
    late_aircraft_delay = round(0.3 * row['num_of_delays_late_aircraft'])
    return weather_delay + nas_delay + late_aircraft_delay

df['delayed_flights_total'] = df.apply(calculate_weather_delay, axis=1)
```

The order is deliberate: **impute the missing Late-Aircraft values first**, because the 30%
rule multiplies that column — feed it `NaN` and every downstream weather total for those rows
is `NaN` too.

## Step 5 — one canonical missing value

*(Paraphrased task: make every flavor of "missing" consistent, all shown as `NaN`, then print
one row of raw JSON showing at least one `NaN`.)*

The payoff. After the numeric `-999` fix back in Step 1, sweep the remaining *string*
sentinels into the same `NaN` so the dataset has exactly one representation of missingness:

```python
df = df.replace(['', ' ', 'NA', 'N/A', 'null', 'None', 'nan'], np.nan)
```

Now `.isna()` finds everything, and the file is finally consistent enough to hand to a model
or a chart.

## Notebook

- [Flights: Missing Data & Rule-Based Imputation](notebooks/flights-data-wrangling.ipynb) —
  all five steps, executed end to end against the public dataset, with the summary table and
  both charts rendered.

## Gotchas

- **A numeric sentinel is the dangerous kind.** A string like `"NA"` at least forces an
  `object` dtype you'll notice; `-999` hides in a numeric column and silently corrupts every
  aggregate. Always scan numeric columns for impossible values before trusting a `.mean()`.
- **Impute before you compute a derived column that depends on the imputed one.** The weather
  reconstruction multiplies the Late-Aircraft column — if that column still has `NaN`s, the
  new column inherits them. Sequence the fills and derivations deliberately.
- **`groupby` silently drops rows with a missing key.** That can be what you want (Step 3) or
  a silent data-loss bug. Decide explicitly, and `dropna(subset=[key])` when it's intentional
  so the intent is on the page.
- **Calendar order is not sort order.** Month and weekday names sort alphabetically unless you
  make them an ordered `Categorical`. Same trap for any ordinal string (`Low`/`Medium`/`High`).
- **`df.apply(..., axis=1)` is row-wise and slow.** Fine here (a few thousand rows), but for
  big frames prefer vectorized/`np.where` logic — reach for row-`apply` only when a rule
  genuinely needs multiple columns of the same row, as the month-dependent rule does.
