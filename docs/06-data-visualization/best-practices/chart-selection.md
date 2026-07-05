# Choosing the Right Chart

## Overview

Selecting the appropriate chart type is one of the most important decisions in data visualization. The right chart makes patterns obvious and insights accessible; the wrong chart obscures the message or misleads the audience. This guide provides a systematic approach to chart selection based on the type of data and the question you're trying to answer.

## The Fundamental Question

Before choosing a chart, ask: **What am I trying to show?**

The answer typically falls into one of these categories:

1. **Comparison**: How do values differ across categories?
2. **Trend**: How have values changed over time?
3. **Distribution**: How are values spread across a range?
4. **Relationship**: How are two or more variables related?
5. **Composition**: What parts make up the whole?
6. **Geospatial**: How do values vary by location?

## Comparison Charts

Use comparison charts when showing differences between discrete categories.

### Bar Chart

**Best for**: Comparing values across categories

**When to use**:
- Comparing discrete categories
- When category labels are text
- When showing rankings
- When values don't sum to a meaningful whole

**Horizontal vs Vertical**:
- Horizontal: Many categories or long labels
- Vertical: Fewer categories, time-related categories

```
Revenue by Product

Product A |=========| $45K
Product B |===============| $62K
Product C |=====| $28K
Product D |===================| $78K
```

**Code example (Python)**:
```python
import matplotlib.pyplot as plt

products = ['Product A', 'Product B', 'Product C', 'Product D']
revenue = [45, 62, 28, 78]

plt.figure(figsize=(10, 6))
plt.barh(products, revenue, color='steelblue')
plt.xlabel('Revenue ($K)')
plt.title('Revenue by Product')
plt.show()
```

### Grouped Bar Chart

**Best for**: Comparing multiple measures across categories

**When to use**:
- Comparing 2-4 measures per category
- When the comparison between groups is important

```
         Q1    Q2    Q3    Q4
Product A: [==] [===] [====] [=====]
Product B: [===] [====] [===] [======]
```

**Avoid when**:
- More than 4 groups per category (too crowded)
- Comparing trends (use line chart instead)

### Stacked Bar Chart

**Best for**: Showing composition AND comparison

**When to use**:
- Showing part-to-whole relationships
- Comparing totals across categories
- When the sum is meaningful

```
Region    Sales Breakdown
North |====|===|==| $100K
South |======|====|===| $130K
East  |===|==|=| $60K
West  |=====|====|==| $110K
       [Online][Store][Phone]
```

**Avoid when**:
- Comparing individual segments across categories (hard to align)
- Too many segments (>5)

### Bullet Chart

**Best for**: Showing a metric against a target

**When to use**:
- Performance against targets
- KPI dashboards
- Replacing gauges/meters

```
Revenue    |========|====> Target: $100K
           [    $82K    ]
           |  Poor  | Fair | Good | Excellent |
```

### Lollipop Chart

**Best for**: Same use as bar chart, but cleaner when many categories

**When to use**:
- Many categories
- When you want to reduce visual weight
- Emphasizing the end point rather than the bar

```
Category A ----o
Category B --------o
Category C ---o
Category D ----------o
```

## Trend Charts

Use trend charts when showing how values change over a continuous dimension (usually time).

### Line Chart

**Best for**: Showing trends over time

**When to use**:
- Continuous time series
- Comparing trends across multiple series
- Emphasizing rate of change

```
Sales Over Time

    |        /\
    |      /    \    /
    |    /        \/
    |  /
    |/
    +-------------------
    Jan  Feb  Mar  Apr
```

**Code example (Python)**:
```python
import matplotlib.pyplot as plt
import pandas as pd

dates = pd.date_range('2024-01-01', periods=12, freq='M')
sales = [100, 120, 115, 130, 145, 160, 155, 170, 180, 175, 190, 210]

plt.figure(figsize=(10, 6))
plt.plot(dates, sales, marker='o', linewidth=2)
plt.xlabel('Month')
plt.ylabel('Sales ($K)')
plt.title('Monthly Sales Trend')
plt.grid(True, alpha=0.3)
plt.show()
```

**Best practices**:
- Start y-axis at zero for magnitude comparisons
- Use markers sparingly (only if few data points)
- Limit to 4-5 lines maximum
- Order legend by end values

### Area Chart

**Best for**: Emphasizing magnitude over time

**When to use**:
- Single series where volume/magnitude matters
- Showing cumulative totals over time

**Avoid when**:
- Multiple overlapping series (obscures data)

### Stacked Area Chart

**Best for**: Showing composition changes over time

**When to use**:
- Part-to-whole over time
- When total and components are both meaningful
- 2-5 categories

```
        _____-----
    ____-----=====~~~~
___-----=====~~~~~####
```

**Avoid when**:
- Comparing individual segments (hard to see non-baseline changes)

### Slope Chart

**Best for**: Comparing values at two points in time

**When to use**:
- Before/after comparisons
- Showing ranking changes
- Emphasizing individual trajectories

```
2020      2024
   \
    \-----> B rises
     \
      \
A ------> A falls
```

## Distribution Charts

Use distribution charts when showing how values are spread across a range.

### Histogram

**Best for**: Showing distribution of a single continuous variable

**When to use**:
- Understanding the shape of data
- Identifying outliers
- Comparing distributions (overlapping histograms)

```
Frequency
    |    ___
    |   |   |
    |  _|   |__
    | |       |_
    |_|         |_
    +---------------
    Low   Value   High
```

**Code example (Python)**:
```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(100, 15, 1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, color='steelblue', edgecolor='white')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution of Values')
plt.show()
```

**Key choices**:
- Bin width: Too few bins hide patterns; too many create noise
- Rule of thumb: sqrt(n) bins, or Sturges' formula

### Box Plot

**Best for**: Comparing distributions across categories

**When to use**:
- Comparing spread and central tendency
- Identifying outliers
- Showing multiple distributions side by side

```
       |--[===|===]--|   o  o  (outliers)
           ^     ^
        Q1/Q3   Median
```

**Shows**:
- Median (center line)
- Interquartile range (box)
- Range/whiskers (typically 1.5 * IQR)
- Outliers (individual points)

### Violin Plot

**Best for**: Showing distribution shape across categories

**When to use**:
- When the shape of the distribution matters
- Comparing multiple distributions
- More detail than box plots

```
        /\
       /  \
      /    \
      |    |
       \  /
        \/
```

### Density Plot (KDE)

**Best for**: Smooth distribution visualization

**When to use**:
- Continuous distribution shape
- Comparing overlapping distributions
- When histogram bins are problematic

### Strip/Swarm Plot

**Best for**: Showing individual data points by category

**When to use**:
- Small to medium datasets
- When individual values matter
- Combined with box or violin plots

## Relationship Charts

Use relationship charts when showing how two or more variables relate to each other.

### Scatter Plot

**Best for**: Showing relationship between two continuous variables

**When to use**:
- Correlation analysis
- Identifying clusters
- Finding outliers
- Regression visualization

```
    Y |    .  . .
      |   . .. .
      |  . . .
      | . . .
      |. .
      +----------
           X
```

**Code example (Python)**:
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(100)
y = 2*x + np.random.randn(100)*0.5

plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6)
plt.xlabel('Variable X')
plt.ylabel('Variable Y')
plt.title('Relationship between X and Y')
plt.show()
```

**Enhancements**:
- Color: Add a third categorical variable
- Size: Add a third continuous variable
- Trend line: Show the relationship mathematically

### Bubble Chart

**Best for**: Scatter plot with a third continuous dimension

**When to use**:
- Three continuous variables
- When the third variable represents magnitude (population, revenue)

**Caution**: Area is harder to judge than position; use sparingly

### Heatmap

**Best for**: Showing patterns in matrix data

**When to use**:
- Correlation matrices
- Pivot table visualization
- Calendar heatmaps
- Geographic density

```
       A     B     C     D
    +-----+-----+-----+-----+
  1 |dark |light|med  |dark |
  2 |light|dark |dark |light|
  3 |med  |med  |light|med  |
```

### Connected Scatter Plot

**Best for**: Showing how two related variables change together over time

**When to use**:
- Two time series that are related
- Showing a trajectory or path

## Composition Charts

Use composition charts when showing parts of a whole.

### Pie Chart

**Best for**: Showing simple proportions

**When to use**:
- Few categories (2-5)
- Proportions are the primary message
- Values sum to 100%

```
        ____
      /      \
     |   60%  |
     |________|
      \  40% /
        ----
```

**Avoid when**:
- More than 5 categories
- Comparing values precisely
- Comparing across multiple pies
- Values don't sum to 100%

**Better alternatives**: Stacked bar, treemap

### Donut Chart

**Best for**: Same as pie chart, with center space for a metric

**When to use**:
- Simple proportions with a key number to highlight
- Dashboard KPIs with breakdown

### Treemap

**Best for**: Hierarchical part-to-whole

**When to use**:
- Many categories
- Nested hierarchies
- Space-efficient composition display

```
+----------------+--------+
|                |        |
|    Category A  | Cat B  |
|                +--------+
|                | C |  D |
+----------------+---+----+
```

### Waterfall Chart

**Best for**: Showing how a starting value changes to an end value

**When to use**:
- Financial statements (revenue to profit)
- Variance analysis
- Sequential additions/subtractions

```
       +---+
       |   |        +---+
Start  | + | - |    |End|
 |     |   |   |    |   |
 |_____|   |___|____|   |
```

### Stacked Bar (100%)

**Best for**: Comparing composition across categories

**When to use**:
- Proportions across categories
- When totals are different but proportions matter

## Geospatial Charts

Use geospatial charts when location is a key dimension.

### Choropleth Map

**Best for**: Showing values by geographic region

**When to use**:
- Values associated with defined regions (countries, states, counties)
- Regional comparisons

**Caution**: Large regions dominate visually regardless of value

### Symbol Map

**Best for**: Showing point-based geographic data

**When to use**:
- Values at specific locations
- Varying magnitude by location
- Avoiding the large-region bias of choropleths

### Bubble Map

**Best for**: Geographic data with magnitude

**When to use**:
- Showing concentration and magnitude
- Population centers, sales locations, etc.

## Decision Framework

### Quick Reference Chart

| Question | Chart Type |
|----------|------------|
| Compare categories | Bar chart |
| Compare over time | Line chart |
| Show distribution | Histogram, box plot |
| Show relationship | Scatter plot |
| Show composition | Pie chart (few), treemap (many) |
| Show geographic | Choropleth, symbol map |
| Track against target | Bullet chart |
| Show flow | Sankey diagram |
| Show ranking | Bar chart, lollipop |
| Compare distributions | Box plot, violin |

### Data Type Considerations

| X Variable | Y Variable | Chart Type |
|------------|------------|------------|
| Categorical | Continuous | Bar, box plot |
| Continuous | Continuous | Scatter, line |
| Categorical | Categorical | Heatmap, grouped bar |
| Time | Continuous | Line, area |
| Geographic | Continuous | Map |

### Audience Considerations

| Audience | Prefer | Avoid |
|----------|--------|-------|
| General public | Bar, line, pie | Violin, heatmap |
| Business users | Bar, line, KPI | Complex statistical |
| Analysts | All types | Over-simplified |
| Executives | Simple KPIs, trends | Dense detail |

## Common Mistakes

### Using Pie Charts for Comparison

**Problem**: Hard to compare slices across multiple pies

**Solution**: Use grouped or stacked bar charts

### 3D Effects

**Problem**: Distorts perception of values

**Solution**: Always use 2D charts

### Dual Y-Axes

**Problem**: Can mislead by implying relationships or misrepresenting scale

**Solution**: Use separate panels, or index values to common scale

### Too Many Series

**Problem**: Line charts with 10+ series are unreadable

**Solution**: Highlight key series, use small multiples

### Truncated Y-Axis

**Problem**: Exaggerates differences

**Solution**: Start at zero, or clearly indicate truncation

### Wrong Chart for the Message

**Problem**: Using a line chart for categorical data implies continuity

**Solution**: Match chart type to data type and message

## Summary

Choosing the right chart requires understanding:

1. **Your data**: Types, relationships, hierarchies
2. **Your question**: Comparison, trend, distribution, relationship, composition
3. **Your audience**: Familiarity with chart types, time available
4. **Your medium**: Print, screen, presentation, dashboard

When in doubt:
- Bar charts for comparison
- Line charts for trends
- Scatter plots for relationships
- Simple is usually better

## Further Reading

- Schwabish, J. (2021). *Better Data Visualizations*
- Knaflic, C. N. (2015). *Storytelling with Data*
- Few, S. (2012). *Show Me the Numbers*
- [From Data to Viz](https://www.data-to-viz.com/) - Interactive chart selection guide
