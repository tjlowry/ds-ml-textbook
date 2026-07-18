# Case Study: The Star Wars Survey

## Summary

This is the flagship wrangling case study of the chapter — my DS 250 Project 5, taking the
**FiveThirtyEight "Star Wars" survey** from a raw Qualtrics export all the way to a feature
matrix a model can train on. It's the best end-to-end example I have of *why* wrangling
matters: the raw file cannot be modeled at all (its columns are literally survey questions),
and every step here is a decision about how to represent messy human survey answers as numbers.

The dataset is the one behind FiveThirtyEight's 2014 article
["America's Favorite 'Star Wars' Movies (And Least Favorite Characters)"](https://fivethirtyeight.com/features/americas-favorite-star-wars-movies-and-least-favorite-characters/).
It's public — I link the
[FiveThirtyEight source](https://github.com/fivethirtyeight/data/tree/master/star-wars-survey)
rather than re-hosting the CSV. Every snippet is from
`~/Projects/school/byui-undergrad/DS_250/Project5/project_5.qmd` (my own, DS 250; mirrored at
`course-files/04-data-wrangling/data_cleaning_starwars.qmd`). The task prompts are the
instructor's; I paraphrase them.

## Step 1 — rename 34 unusable columns

The export uses the full survey *question* as each column header, and where a question had
multiple sub-answers, pandas names the overflow columns `Unnamed: 4`, `Unnamed: 5`, and so on.
None of it is usable. A rename dictionary maps every original name to a short, tidy
`snake_case` one:

```python
names = {
    'RespondentID': 'response_id',
    'Have you seen any of the 6 films in the Star Wars franchise?': 'seen_all',
    'Do you consider yourself to be a fan of the Star Wars film franchise?': 'fan',
    'Which of the following Star Wars films have you seen? Please select all that apply.': 'watch_ep1',
    'Unnamed: 4': 'watch_ep2',
    'Unnamed: 5': 'watch_ep3',
    # ... episodes, character-favorability columns, demographics ...
    'Location (Census Region)': 'region',
    'Which character shot first?': 'shot_first',
}
df = df.rename(columns=names)
```

With readable names in place, I collapse the "have you seen episode N?" columns — which arrive
as the full movie title or `NaN` — into a clean `yes`/`no`, and drop the header row of
sub-question labels:

```python
df.loc[df['watch_ep1'] == 'Star Wars: Episode I  The Phantom Menace', 'watch_ep1'] = 'yes'
# ... same for episodes II-VI ...
df.fillna('no', inplace=True)
df = df.drop(df.index[0])
```

## Step 2 — ordinal encoding

Several survey answers are **ordered categories** — age brackets, education levels, income
bands. These carry an order (a `>60` respondent is "more" than an `18-29` one), so the right
encoding is a single ordinal number, not one-hot. I map each band to an integer and drop the
original text column:

```python
age_mapping = {'18-29': 1, '30-44': 2, '45-60': 3, '>60': 4}
df['age_group'] = df['age'].map(age_mapping)
df.drop('age', axis=1, inplace=True)

income_mapping = {
    '$0 - $24,999': 1, '$25,000 - $49,99': 2, '$50,000 - $99,999': 3,
    '$100,000 - $149,999': 4, '$150,000+': 5, 'no': 6,   # 'no' = missing sentinel
}
df['income_group'] = df['house_income'].map(income_mapping)
df.drop('house_income', axis=1, inplace=True)
```

Education gets the same treatment. Note the `'no'` → `6` mapping: earlier I filled missing
values with the string `'no'`, so it needs a code too — and it becomes the "this is missing"
bucket I have to exclude later.

## Step 3 — build the target column

*(Paraphrased task: create the model's target — whether a respondent makes more than $50k —
from the income column.)*

The target `y` is a wrangling artifact as much as the features are. Income band `3` is
`$50,000-$99,999`, so ">$50k" is bands 3–5 — but I have to **exclude band 6**, since that's
the missing-value bucket, not a real high income. Hence the `x >= 3 and x < 6`:

```python
df['target'] = df['income_group'].astype(float).apply(
    lambda x: 1 if (x >= 3 and x < 6) else 0)
```

The `.astype(float)` is the [dtype gotcha](pandas-fundamentals.md#dtype-casting) in action —
the column was `object` because of the text sentinel, and the comparison needs a number.

## Step 4 — one-hot encoding

The remaining categoricals are **unordered** — Census region, "who shot first," yes/no
questions. Those get one-hot encoded (a column per category) rather than an ordinal code,
because there's no meaningful order to preserve. `pd.get_dummies` does the expansion;
`drop_first=True` avoids the dummy-variable trap, and `dummy_na=True` keeps "missing" as its
own explicit category:

```python
df = pd.get_dummies(df, columns=['region'], dummy_na=True, drop_first=True)
df = pd.get_dummies(df, columns=['shot_first'], drop_first=True, dummy_na=True)
df = df.replace({True: 1, False: 0})   # booleans -> 0/1 for the model

# The straightforward yes/no columns just get a binary map
for col in ['star_trek_fan', 'eu_know', 'eu_fan', 'seen_all', 'fan']:
    df[col] = df[col].map({'Yes': 1, 'No': 0})
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})
```

At this point the frame is entirely numeric — no strings left anywhere — which is the actual
finish line of "wrangling": a table a model can consume.

## Step 5 — where wrangling hands off to modeling

The reason this case study is the chapter's flagship is that it runs straight from raw CSV into
a model with no gap. Once the frame is numeric, I check feature correlations against the
target, pick features, and train a `RandomForestClassifier`:

```python
df.dropna(inplace=True)

feature_cols = ['fan', 'edu_group', 'region_West North Central', 'region_Mountain',
                'region_Middle Atlantic', 'eu_fan', 'region_Pacific']
X = df[feature_cols]
y = df.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
clf = RandomForestClassifier().fit(X_train, y_train)
y_pred = clf.predict(X_test)
```

The model predicts whether a respondent earns >$50k with accuracy, precision, and recall all
right around 80%, and the most useful features are `fan`, `edu_group`, and `region_Pacific`.

> **In modern ML.** Steps 2–4 above — ordinal encoding, target construction, one-hot
> encoding — are exactly the *feature engineering* an ML pipeline does before fitting. There's
> no clean line between "wrangling" and "modeling": the encoding choices here decide what the
> model can learn. The model itself (train/test split, `RandomForestClassifier`, and reading
> feature importances) is covered in the
> [Machine Learning chapter](../08-machine-learning/classification/random-forests.md); this
> page is the data-preparation half of that same story.

## Notebook

There's no separate notebook for this case study — the Quarto source
(`data_cleaning_starwars.qmd`) already serves that role, self-contained with its own rendered
output. Open it in a Quarto-capable editor, or read the code inline above. The two published
FiveThirtyEight charts I recreated in Altair (percent who've seen each film; percent ranking
each film #1) are in that source.

## Gotchas

- **Ordinal vs. one-hot is a real modeling decision, not a formality.** Ordinal-encode when
  the categories have an order (income bands), one-hot when they don't (Census region).
  Getting it backwards tells the model a false ordering (`Pacific > Mountain`) or throws away
  a real one.
- **A missing-value bucket masquerades as a real category.** Filling missing income with
  `'no'` → `6` was convenient, but `6` then looks like the *highest* income band. The
  `x < 6` guard in the target is there purely to exclude it — miss that and every
  missing-income respondent gets labeled high-earner.
- **`drop_first=True` matters for linear models, less for trees.** One-hot without it creates
  perfectly collinear dummies (the dummy-variable trap). A random forest tolerates it, but
  it's the right default habit and keeps the feature matrix smaller.
- **`dummy_na=True` or you lose information.** Without it, `get_dummies` drops `NaN` rows to
  all-zeros, silently conflating "missing" with "none of the categories." Keep missingness
  explicit.
- **`get_dummies` column names carry the category value.** That's why a feature is named
  `region_Pacific` — handy for reading importances, but it means the exact string in the data
  (`'West North Central'`, spaces and all) becomes part of your column name. Rename downstream
  if that's awkward.
