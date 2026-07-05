# Plotly for Interactive Visualizations

## Overview

Plotly is a powerful library for creating interactive, publication-quality visualizations. Unlike static Matplotlib plots, Plotly charts allow users to zoom, pan, hover for details, and interact with the data. Plotly works in Jupyter notebooks, standalone HTML files, and can be embedded in web applications.

## Why Plotly?

- **Interactivity**: Built-in zoom, pan, hover tooltips, and click events
- **Web-native**: Outputs to HTML/JavaScript for easy sharing
- **Multiple interfaces**: High-level Plotly Express and detailed Graph Objects
- **Dashboard integration**: Works with Dash for building data applications

## Two Interfaces

Plotly offers two APIs:

1. **Plotly Express (`px`)**: High-level, concise syntax for common plots
2. **Graph Objects (`go`)**: Low-level, complete control over every element

## Plotly Express Basics

### Setup

```python
import plotly.express as px
import pandas as pd
import numpy as np

# Plotly includes several built-in datasets
df = px.data.tips()
gapminder = px.data.gapminder()
iris = px.data.iris()
stocks = px.data.stocks()
```

### Scatter Plots

```python
import plotly.express as px

df = px.data.tips()

# Basic scatter plot
fig = px.scatter(df, x="total_bill", y="tip")
fig.show()
```

**Visual description**: An interactive scatter plot appears with total bill on the x-axis and tip on the y-axis. Hovering over any point shows the exact values.

### Adding Dimensions

```python
import plotly.express as px

df = px.data.tips()

fig = px.scatter(
    df,
    x="total_bill",
    y="tip",
    color="smoker",           # Color by category
    size="size",              # Size by numeric value
    symbol="sex",             # Shape by category
    hover_data=["day"],       # Extra info on hover
    title="Tips Analysis"
)

fig.update_layout(
    xaxis_title="Total Bill ($)",
    yaxis_title="Tip ($)"
)

fig.show()
```

**Visual description**: Points are colored by smoker status, sized by party size, and shaped by sex. Hovering reveals all data including the day.

### Line Charts

```python
import plotly.express as px

stocks = px.data.stocks()

fig = px.line(
    stocks,
    x="date",
    y=["GOOG", "AAPL", "AMZN", "FB", "NFLX", "MSFT"],
    title="Stock Prices Over Time"
)

fig.update_layout(
    yaxis_title="Price (normalized)",
    legend_title="Company",
    hovermode="x unified"     # Show all values at x position
)

fig.show()
```

**Visual description**: Multiple line traces for each stock, with a unified hover showing all values at each date.

### Bar Charts

```python
import plotly.express as px

df = px.data.tips()

# Grouped bar chart
fig = px.bar(
    df,
    x="day",
    y="total_bill",
    color="sex",
    barmode="group",          # "group", "stack", "overlay", "relative"
    title="Total Bills by Day and Sex"
)

fig.show()
```

### Histograms

```python
import plotly.express as px

df = px.data.tips()

fig = px.histogram(
    df,
    x="total_bill",
    color="time",
    nbins=30,
    marginal="box",           # "rug", "box", "violin"
    opacity=0.7,
    title="Distribution of Total Bills"
)

fig.show()
```

**Visual description**: Overlapping histograms for lunch and dinner with box plots shown in the margin above.

### Box Plots

```python
import plotly.express as px

df = px.data.tips()

fig = px.box(
    df,
    x="day",
    y="total_bill",
    color="smoker",
    notched=True,             # Show confidence interval
    points="outliers",        # "all", "outliers", False
    title="Bill Distribution by Day"
)

fig.show()
```

### Violin Plots

```python
import plotly.express as px

df = px.data.tips()

fig = px.violin(
    df,
    x="day",
    y="total_bill",
    color="sex",
    box=True,                 # Show box plot inside
    points="all",             # Show all data points
    title="Bill Distribution (Violin)"
)

fig.show()
```

### Heatmaps

```python
import plotly.express as px
import pandas as pd
import numpy as np

# Create correlation matrix
df = px.data.tips()
corr = df[['total_bill', 'tip', 'size']].corr()

fig = px.imshow(
    corr,
    text_auto=".2f",          # Show values with 2 decimals
    color_continuous_scale="RdBu_r",
    aspect="auto",
    title="Correlation Heatmap"
)

fig.show()
```

### Pie and Donut Charts

```python
import plotly.express as px

df = px.data.tips()
day_counts = df['day'].value_counts().reset_index()
day_counts.columns = ['day', 'count']

# Pie chart
fig = px.pie(
    day_counts,
    values="count",
    names="day",
    title="Meals by Day",
    hole=0.3                  # Set > 0 for donut chart
)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
```

### Scatter Matrix (Pair Plot)

```python
import plotly.express as px

iris = px.data.iris()

fig = px.scatter_matrix(
    iris,
    dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    color="species",
    title="Iris Dataset Scatter Matrix"
)

fig.update_traces(diagonal_visible=False)
fig.show()
```

**Visual description**: A grid of scatter plots showing all pairwise relationships between iris measurements, colored by species.

## Animated Visualizations

### Animated Scatter Plot

```python
import plotly.express as px

gapminder = px.data.gapminder()

fig = px.scatter(
    gapminder,
    x="gdpPercap",
    y="lifeExp",
    animation_frame="year",       # Animate over years
    animation_group="country",    # Track countries
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=55,
    range_x=[100, 100000],
    range_y=[25, 90],
    title="Gapminder: Life Expectancy vs GDP"
)

fig.show()
```

**Visual description**: An animated bubble chart with a play button. Each bubble represents a country, moving as GDP and life expectancy change from 1952 to 2007.

### Animated Bar Chart

```python
import plotly.express as px

gapminder = px.data.gapminder()

# Filter to specific countries
countries = ['United States', 'China', 'India', 'Japan', 'Germany']
df = gapminder[gapminder['country'].isin(countries)]

fig = px.bar(
    df,
    x="country",
    y="pop",
    color="country",
    animation_frame="year",
    range_y=[0, 1.5e9],
    title="Population Growth Over Time"
)

fig.show()
```

## Geographic Visualizations

### Choropleth Maps

```python
import plotly.express as px

gapminder = px.data.gapminder()
df_2007 = gapminder[gapminder['year'] == 2007]

fig = px.choropleth(
    df_2007,
    locations="iso_alpha",        # Country codes
    color="lifeExp",
    hover_name="country",
    color_continuous_scale="Viridis",
    title="Life Expectancy by Country (2007)"
)

fig.show()
```

**Visual description**: A world map with countries colored by life expectancy. Hovering over a country shows its name and exact value.

### Scatter on Maps

```python
import plotly.express as px

gapminder = px.data.gapminder()
df_2007 = gapminder[gapminder['year'] == 2007]

fig = px.scatter_geo(
    df_2007,
    locations="iso_alpha",
    size="pop",
    color="continent",
    hover_name="country",
    projection="natural earth",
    title="World Population (2007)"
)

fig.show()
```

### US State Maps

```python
import plotly.express as px
import pandas as pd

# Sample state data
df = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
    'value': [39, 29, 21, 19, 13, 12, 11, 10, 10, 10]
})

fig = px.choropleth(
    df,
    locations="state",
    locationmode="USA-states",
    color="value",
    scope="usa",
    color_continuous_scale="Blues",
    title="Sample US State Data"
)

fig.show()
```

## Graph Objects for Fine Control

For complete customization, use `plotly.graph_objects`:

### Basic Structure

```python
import plotly.graph_objects as go
import numpy as np

# Create figure
fig = go.Figure()

# Add traces
x = np.linspace(0, 10, 100)

fig.add_trace(go.Scatter(
    x=x,
    y=np.sin(x),
    mode='lines',
    name='sin(x)',
    line=dict(color='blue', width=2)
))

fig.add_trace(go.Scatter(
    x=x,
    y=np.cos(x),
    mode='lines',
    name='cos(x)',
    line=dict(color='red', width=2, dash='dash')
))

# Update layout
fig.update_layout(
    title='Trigonometric Functions',
    xaxis_title='x',
    yaxis_title='y',
    legend_title='Function',
    template='plotly_white'
)

fig.show()
```

### Multiple Subplots

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Create subplot grid
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Line Plot', 'Scatter Plot', 'Bar Chart', 'Histogram'),
    specs=[
        [{"type": "scatter"}, {"type": "scatter"}],
        [{"type": "bar"}, {"type": "histogram"}]
    ]
)

x = np.linspace(0, 10, 50)

# Line plot (row 1, col 1)
fig.add_trace(
    go.Scatter(x=x, y=np.sin(x), mode='lines', name='Line'),
    row=1, col=1
)

# Scatter plot (row 1, col 2)
fig.add_trace(
    go.Scatter(x=np.random.rand(50), y=np.random.rand(50),
               mode='markers', name='Scatter'),
    row=1, col=2
)

# Bar chart (row 2, col 1)
fig.add_trace(
    go.Bar(x=['A', 'B', 'C', 'D'], y=[3, 7, 2, 5], name='Bar'),
    row=2, col=1
)

# Histogram (row 2, col 2)
fig.add_trace(
    go.Histogram(x=np.random.randn(500), name='Histogram'),
    row=2, col=2
)

fig.update_layout(height=600, width=800, title_text="Multiple Subplots")
fig.show()
```

### Dual Y-Axes

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

x = np.arange(1, 13)
revenue = [10, 12, 14, 18, 22, 28, 32, 35, 30, 25, 20, 15]
growth = [None, 20, 16.7, 28.6, 22.2, 27.3, 14.3, 9.4, -14.3, -16.7, -20, -25]

# Revenue on primary axis
fig.add_trace(
    go.Bar(x=x, y=revenue, name="Revenue ($M)", marker_color='steelblue'),
    secondary_y=False
)

# Growth rate on secondary axis
fig.add_trace(
    go.Scatter(x=x, y=growth, name="Growth (%)",
               mode='lines+markers', marker_color='coral'),
    secondary_y=True
)

fig.update_layout(title_text="Revenue and Growth Rate")
fig.update_xaxes(title_text="Month", tickvals=list(range(1, 13)),
                 ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
fig.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
fig.update_yaxes(title_text="Growth (%)", secondary_y=True)

fig.show()
```

### 3D Plots

```python
import plotly.graph_objects as go
import numpy as np

# 3D Surface
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])

fig.update_layout(
    title='3D Surface Plot',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

fig.show()
```

**Visual description**: An interactive 3D surface that can be rotated and zoomed. The surface shows a ripple pattern emanating from the center.

### 3D Scatter

```python
import plotly.graph_objects as go
import numpy as np

# Generate 3D data
np.random.seed(42)
n = 200
x = np.random.randn(n)
y = np.random.randn(n)
z = np.random.randn(n)
colors = np.random.rand(n)

fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=colors,
        colorscale='Viridis',
        opacity=0.8
    )
)])

fig.update_layout(title='3D Scatter Plot')
fig.show()
```

## Customization

### Themes/Templates

```python
import plotly.express as px
import plotly.io as pio

# Available templates
print(pio.templates)
# ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white',
#  'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']

df = px.data.tips()

# Using a template
fig = px.scatter(df, x="total_bill", y="tip", color="day",
                 template="plotly_dark",
                 title="Dark Theme Example")
fig.show()
```

### Custom Colors

```python
import plotly.express as px

df = px.data.tips()

# Using discrete color sequence
fig = px.bar(
    df, x="day", y="total_bill", color="sex",
    color_discrete_sequence=["#636EFA", "#EF553B"],  # Custom colors
    title="Custom Discrete Colors"
)
fig.show()

# Using continuous color scale
fig2 = px.scatter(
    df, x="total_bill", y="tip", color="size",
    color_continuous_scale="Plasma",  # Or: "Viridis", "Cividis", "Inferno", etc.
    title="Custom Continuous Colors"
)
fig2.show()
```

### Annotations and Shapes

```python
import plotly.graph_objects as go
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='sin(x)'))

# Add annotation
fig.add_annotation(
    x=np.pi/2,
    y=1,
    text="Maximum",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#636363",
    ax=40,
    ay=-40
)

# Add horizontal line
fig.add_hline(y=0, line_dash="dash", line_color="gray")

# Add vertical rectangle (shaded region)
fig.add_vrect(
    x0=np.pi/4, x1=3*np.pi/4,
    fillcolor="LightSalmon", opacity=0.3,
    line_width=0,
    annotation_text="Peak Region"
)

fig.update_layout(title="Annotations and Shapes")
fig.show()
```

### Hover Templates

```python
import plotly.express as px

df = px.data.tips()

fig = px.scatter(
    df, x="total_bill", y="tip", color="day",
    hover_data={
        'total_bill': ':.2f',     # Format as 2 decimal places
        'tip': ':.2f',
        'size': True,             # Include size
        'day': False              # Hide day (already in color legend)
    }
)

# Custom hover template
fig.update_traces(
    hovertemplate="<b>Bill:</b> $%{x:.2f}<br>" +
                  "<b>Tip:</b> $%{y:.2f}<br>" +
                  "<b>Party Size:</b> %{customdata[0]}<extra></extra>"
)

fig.show()
```

## Saving and Exporting

### Save as HTML

```python
import plotly.express as px

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip")

# Interactive HTML file
fig.write_html("plot.html")

# HTML with embedded Plotly.js (larger but self-contained)
fig.write_html("plot_standalone.html", include_plotlyjs=True)
```

### Save as Static Image

```python
import plotly.express as px

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip")

# Requires kaleido: pip install -U kaleido
fig.write_image("plot.png", scale=2)    # PNG at 2x resolution
fig.write_image("plot.svg")             # SVG vector format
fig.write_image("plot.pdf")             # PDF vector format
```

### Save as JSON

```python
import plotly.express as px
import plotly.io as pio

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip")

# Save figure specification as JSON
fig.write_json("plot.json")

# Load and recreate
fig_loaded = pio.read_json("plot.json")
fig_loaded.show()
```

## Integration with Dash

Plotly figures integrate seamlessly with Dash for building web applications:

```python
# Basic Dash app structure (requires: pip install dash)
from dash import Dash, html, dcc
import plotly.express as px

app = Dash(__name__)

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", color="day")

app.layout = html.Div([
    html.H1("My Dashboard"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Summary

| Feature | Plotly Express | Graph Objects |
|---------|----------------|---------------|
| Syntax | Concise, DataFrame-focused | Verbose, complete control |
| Best for | Quick exploration, standard charts | Complex customization, dashboards |
| Learning curve | Low | Medium-High |
| Flexibility | Good | Excellent |

| Plot Type | Function | Use Case |
|-----------|----------|----------|
| `px.scatter` | Scatter plots | Relationships, distributions |
| `px.line` | Line charts | Time series, trends |
| `px.bar` | Bar charts | Category comparisons |
| `px.histogram` | Histograms | Distributions |
| `px.box` / `px.violin` | Box/Violin plots | Distribution comparisons |
| `px.choropleth` | Maps | Geographic data |
| `px.scatter_3d` | 3D scatter | Three-variable relationships |
| `px.imshow` | Heatmaps | Matrix visualization |
| `px.scatter_matrix` | Pair plots | Multi-variable exploration |

## Further Reading

- [Plotly Python Documentation](https://plotly.com/python/)
- [Plotly Express API Reference](https://plotly.com/python-api-reference/plotly.express.html)
- [Dash Documentation](https://dash.plotly.com/)
- [Plotly Community Forum](https://community.plotly.com/)
