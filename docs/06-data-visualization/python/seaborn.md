# Seaborn for Statistical Plots

## Overview

Seaborn is a Python data visualization library built on top of Matplotlib. It provides a high-level interface for creating attractive and informative statistical graphics. Seaborn excels at visualizing relationships in data, distributions, and categorical comparisons with minimal code.

## Why Seaborn?

- **Statistical focus**: Built-in support for statistical aggregations and confidence intervals
- **Pandas integration**: Works seamlessly with DataFrames
- **Attractive defaults**: Beautiful color palettes and themes out of the box
- **Complex visualizations**: Multi-plot grids and pair plots with single function calls

## Setup and Data

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set the default style
sns.set_theme(style="whitegrid")

# Seaborn includes several built-in datasets
tips = sns.load_dataset("tips")
iris = sns.load_dataset("iris")
titanic = sns.load_dataset("titanic")
penguins = sns.load_dataset("penguins")
```

## Relational Plots

Relational plots show the relationship between two or more variables.

### Scatter Plots with `scatterplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

# Basic scatter plot
sns.scatterplot(data=tips, x="total_bill", y="tip", ax=ax)
ax.set_title("Tips vs Total Bill")

plt.show()
```

### Adding Dimensions with Color and Size

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

# Encode additional variables with hue, size, and style
sns.scatterplot(
    data=tips,
    x="total_bill",
    y="tip",
    hue="time",        # Color by time of day
    size="size",       # Size by party size
    style="smoker",    # Shape by smoker status
    palette="deep",
    ax=ax
)

ax.set_title("Tips Analysis: Multiple Dimensions")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()
```

### Line Plots with `lineplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create time series data
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=100, freq='D')
df = pd.DataFrame({
    'date': np.tile(dates, 2),
    'value': np.concatenate([
        np.cumsum(np.random.randn(100)) + 10,
        np.cumsum(np.random.randn(100)) + 15
    ]),
    'category': ['A'] * 100 + ['B'] * 100
})

fig, ax = plt.subplots(figsize=(12, 6))

# Line plot with confidence intervals (shown by default)
sns.lineplot(data=df, x="date", y="value", hue="category", ax=ax)

ax.set_title("Time Series with Confidence Intervals")
ax.set_xlabel("Date")
ax.set_ylabel("Value")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### `relplot()` for Faceted Relational Plots

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# Create faceted scatter plots
g = sns.relplot(
    data=tips,
    x="total_bill",
    y="tip",
    hue="smoker",
    col="time",        # Facet by column
    row="sex",         # Facet by row
    height=4,
    aspect=1.2
)

g.fig.suptitle("Tips by Time and Gender", y=1.02)
plt.show()
```

## Distribution Plots

Distribution plots show the distribution of one or more variables.

### Histograms with `histplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Basic histogram
sns.histplot(data=tips, x="total_bill", ax=axes[0])
axes[0].set_title("Basic Histogram")

# With KDE overlay
sns.histplot(data=tips, x="total_bill", kde=True, ax=axes[1])
axes[1].set_title("Histogram with KDE")

# Grouped histogram
sns.histplot(data=tips, x="total_bill", hue="time", ax=axes[2])
axes[2].set_title("Grouped by Time")

plt.tight_layout()
plt.show()
```

### KDE Plots with `kdeplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 1D KDE
sns.kdeplot(data=tips, x="total_bill", hue="time", fill=True, ax=axes[0])
axes[0].set_title("1D KDE Plot")

# 2D KDE (density contours)
sns.kdeplot(data=tips, x="total_bill", y="tip", hue="time", ax=axes[1])
axes[1].set_title("2D KDE Plot")

plt.tight_layout()
plt.show()
```

### ECDF Plots with `ecdfplot()`

The Empirical Cumulative Distribution Function shows what proportion of data falls below each value:

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

sns.ecdfplot(data=tips, x="total_bill", hue="time", ax=ax)
ax.set_title("ECDF of Total Bill by Time")
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Median')
ax.legend()

plt.show()
```

### Rug Plots with `rugplot()`

Rug plots show individual data points along an axis:

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

sns.kdeplot(data=tips, x="total_bill", fill=True, ax=ax)
sns.rugplot(data=tips, x="total_bill", height=0.05, ax=ax)

ax.set_title("KDE with Rug Plot")
plt.show()
```

### `displot()` for Faceted Distribution Plots

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

g = sns.displot(
    data=tips,
    x="total_bill",
    hue="smoker",
    col="time",
    kind="kde",        # "hist", "kde", or "ecdf"
    fill=True,
    height=4,
    aspect=1.3
)

g.fig.suptitle("Distribution of Bills by Time and Smoker Status", y=1.02)
plt.show()
```

## Categorical Plots

Categorical plots show distributions and comparisons across categories.

### Box Plots with `boxplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

sns.boxplot(data=tips, x="day", y="total_bill", hue="time", ax=ax)

ax.set_title("Total Bill by Day and Time")
plt.show()
```

### Violin Plots with `violinplot()`

Violin plots combine box plots with KDE:

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

sns.violinplot(
    data=tips,
    x="day",
    y="total_bill",
    hue="sex",
    split=True,        # Split violins for comparison
    inner="quart",     # Show quartiles inside
    ax=ax
)

ax.set_title("Total Bill Distribution by Day and Sex")
plt.show()
```

### Strip and Swarm Plots

Show individual data points:

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Strip plot (with jitter)
sns.stripplot(data=tips, x="day", y="total_bill", hue="time",
              dodge=True, alpha=0.6, ax=axes[0])
axes[0].set_title("Strip Plot")

# Swarm plot (no overlap)
sns.swarmplot(data=tips, x="day", y="total_bill", hue="time",
              dodge=True, ax=axes[1])
axes[1].set_title("Swarm Plot")

plt.tight_layout()
plt.show()
```

### Bar Plots with `barplot()`

Seaborn bar plots show the mean and confidence interval:

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    data=tips,
    x="day",
    y="total_bill",
    hue="sex",
    errorbar="sd",     # Show standard deviation
    ax=ax
)

ax.set_title("Mean Total Bill by Day and Sex (with SD)")
plt.show()
```

### Count Plots with `countplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

titanic = sns.load_dataset("titanic")

fig, ax = plt.subplots(figsize=(10, 6))

sns.countplot(data=titanic, x="class", hue="survived", ax=ax)

ax.set_title("Survival Count by Passenger Class")
ax.legend(title="Survived", labels=["No", "Yes"])

plt.show()
```

### Point Plots with `pointplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))

sns.pointplot(
    data=tips,
    x="day",
    y="total_bill",
    hue="sex",
    markers=["o", "s"],
    linestyles=["-", "--"],
    ax=ax
)

ax.set_title("Mean Total Bill by Day and Sex")
plt.show()
```

### `catplot()` for Faceted Categorical Plots

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

g = sns.catplot(
    data=tips,
    x="day",
    y="total_bill",
    hue="sex",
    col="time",
    kind="box",        # "strip", "swarm", "box", "violin", "boxen", "point", "bar", "count"
    height=5,
    aspect=1
)

g.fig.suptitle("Bill Distribution by Day, Sex, and Time", y=1.02)
plt.show()
```

## Matrix Plots

### Heatmaps with `heatmap()`

```python
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Create correlation matrix
tips = sns.load_dataset("tips")
corr = tips[['total_bill', 'tip', 'size']].corr()

fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(
    corr,
    annot=True,           # Show values
    fmt=".2f",            # Format as 2 decimal places
    cmap="coolwarm",      # Color palette
    center=0,             # Center colormap at 0
    square=True,          # Square cells
    linewidths=0.5,       # Cell border width
    ax=ax
)

ax.set_title("Correlation Heatmap")
plt.show()
```

### Cluster Maps with `clustermap()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Get iris data and create summary
iris = sns.load_dataset("iris")
iris_means = iris.groupby("species").mean()

g = sns.clustermap(
    iris_means,
    cmap="viridis",
    standard_scale=1,    # Standardize columns
    figsize=(8, 6),
    annot=True,
    fmt=".1f"
)

g.fig.suptitle("Iris Species Clustering", y=1.02)
plt.show()
```

## Multi-Plot Grids

### Pair Plots with `pairplot()`

Pair plots show pairwise relationships between all numeric variables:

```python
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")

g = sns.pairplot(
    iris,
    hue="species",
    diag_kind="kde",     # "hist" or "kde" on diagonal
    corner=False,        # Show full matrix
    plot_kws={"alpha": 0.6}
)

g.fig.suptitle("Iris Dataset Pairplot", y=1.02)
plt.show()
```

### Joint Plots with `jointplot()`

Joint plots combine bivariate and univariate distributions:

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

g = sns.jointplot(
    data=tips,
    x="total_bill",
    y="tip",
    kind="reg",          # "scatter", "kde", "hist", "hex", "reg", "resid"
    height=8
)

g.fig.suptitle("Tips vs Total Bill with Regression", y=1.02)
plt.show()
```

### FacetGrid for Custom Multi-Plot Grids

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# Create the grid
g = sns.FacetGrid(tips, col="time", row="smoker", height=4, aspect=1.2)

# Map a plot to each facet
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip", hue="sex")

# Add legend and titles
g.add_legend()
g.fig.suptitle("Tips by Time and Smoker Status", y=1.02)

plt.show()
```

### PairGrid for Custom Pair Plots

```python
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")

g = sns.PairGrid(iris, hue="species", diag_sharey=False)

# Different plots for different positions
g.map_upper(sns.scatterplot, alpha=0.6)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot, kde=True)

g.add_legend()
g.fig.suptitle("Custom Pair Grid", y=1.02)

plt.show()
```

## Regression Plots

### `regplot()` and `lmplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Basic regression plot
sns.regplot(data=tips, x="total_bill", y="tip", ax=axes[0])
axes[0].set_title("Linear Regression")

# Polynomial regression
sns.regplot(data=tips, x="total_bill", y="tip", order=2, ax=axes[1])
axes[1].set_title("Polynomial Regression (order=2)")

plt.tight_layout()
plt.show()
```

### Faceted Regression with `lmplot()`

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

g = sns.lmplot(
    data=tips,
    x="total_bill",
    y="tip",
    hue="smoker",
    col="time",
    height=5,
    aspect=1
)

g.fig.suptitle("Tips Regression by Time and Smoker Status", y=1.02)
plt.show()
```

## Themes and Aesthetics

### Built-in Themes

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# Available themes: darkgrid, whitegrid, dark, white, ticks
themes = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']

fig, axes = plt.subplots(1, 5, figsize=(20, 4))

for ax, theme in zip(axes, themes):
    with sns.axes_style(theme):
        sns.histplot(data=tips, x="total_bill", ax=ax)
        ax.set_title(f'Theme: {theme}')

plt.tight_layout()
plt.show()
```

### Color Palettes

```python
import seaborn as sns
import matplotlib.pyplot as plt

# View a palette
sns.palplot(sns.color_palette("husl", 8))
plt.title("husl palette")
plt.show()

# Available palettes
palettes = ['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind']

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

tips = sns.load_dataset("tips")

for ax, palette in zip(axes.flat, palettes):
    sns.barplot(data=tips, x="day", y="total_bill", hue="sex",
                palette=palette, ax=ax)
    ax.set_title(f'Palette: {palette}')
    ax.legend([], [], frameon=False)  # Hide legend for clarity

plt.tight_layout()
plt.show()
```

### Setting Context for Different Output Sizes

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# Contexts: paper, notebook, talk, poster
contexts = ['paper', 'notebook', 'talk', 'poster']

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for ax, context in zip(axes.flat, contexts):
    with sns.plotting_context(context):
        sns.lineplot(data=tips, x="size", y="total_bill", ax=ax)
        ax.set_title(f'Context: {context}')

plt.tight_layout()
plt.show()
```

### Custom Styling

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Set custom theme
sns.set_theme(
    style="whitegrid",
    palette="deep",
    font="sans-serif",
    font_scale=1.2,
    rc={
        "axes.facecolor": "#f8f9fa",
        "figure.facecolor": "white",
        "grid.color": "#dee2e6",
        "grid.linewidth": 0.5
    }
)

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=tips, x="day", y="total_bill", hue="time", ax=ax)
ax.set_title("Custom Styled Plot")

plt.show()

# Reset to defaults
sns.reset_defaults()
```

## Summary

| Plot Type | Function | Use Case |
|-----------|----------|----------|
| Scatter | `scatterplot()` | Relationship between two continuous variables |
| Line | `lineplot()` | Trends over continuous variable (time series) |
| Histogram | `histplot()` | Distribution of a single variable |
| KDE | `kdeplot()` | Smooth density estimation |
| Box | `boxplot()` | Distribution summary with quartiles |
| Violin | `violinplot()` | Distribution shape with density |
| Bar | `barplot()` | Mean comparison with confidence intervals |
| Count | `countplot()` | Frequency of categorical values |
| Heatmap | `heatmap()` | Matrix visualization (correlations) |
| Pair | `pairplot()` | All pairwise relationships |
| Joint | `jointplot()` | Bivariate + marginal distributions |
| Regression | `regplot()`/`lmplot()` | Linear relationships with fit |

## Further Reading

- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)
