# Matplotlib Fundamentals

## Overview

Matplotlib is the foundational plotting library for Python. Nearly every other Python visualization library builds upon or integrates with Matplotlib. Understanding its architecture and API is essential for creating publication-quality figures and customizing visualizations to meet specific requirements.

## The Figure and Axes Model

Matplotlib uses a hierarchical structure where a **Figure** contains one or more **Axes** (individual plots). Understanding this distinction is crucial for creating complex visualizations.

### Figure

The Figure is the top-level container that holds everything you see in a visualization. It controls:

- Overall size and resolution (DPI)
- Background color
- The arrangement of all subplots
- Saving to files

### Axes

An Axes object is an individual plot within a Figure. Despite the potentially confusing name, an Axes represents a complete plot with:

- X and Y axis (or more for 3D plots)
- Data visualization elements (lines, bars, scatter points)
- Labels, titles, and legends
- Tick marks and grid lines

```python
import matplotlib.pyplot as plt
import numpy as np

# Create a Figure and Axes
fig, ax = plt.subplots(figsize=(10, 6))

# The figure controls the overall canvas
# The axes is where we plot data
```

## Two Interfaces: pyplot vs Object-Oriented

Matplotlib offers two ways to create plots:

### pyplot Interface (State-Based)

The pyplot interface is simpler for quick plots but less flexible:

```python
import matplotlib.pyplot as plt

# pyplot manages the current figure and axes implicitly
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Simple Plot')
plt.show()
```

### Object-Oriented Interface (Recommended)

The OO interface provides explicit control and is better for complex visualizations:

```python
import matplotlib.pyplot as plt
import numpy as np

# Explicitly create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Work directly with the axes object
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_title('Trigonometric Functions')
ax.legend()

plt.tight_layout()
plt.show()
```

## Basic Plot Types

### Line Plots

Line plots connect data points with lines, ideal for showing trends over continuous variables:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 50)
y1 = x ** 2
y2 = x ** 1.5

ax.plot(x, y1, color='blue', linestyle='-', linewidth=2, label='Quadratic')
ax.plot(x, y2, color='red', linestyle='--', linewidth=2, label='Power 1.5')

ax.set_xlabel('X Values')
ax.set_ylabel('Y Values')
ax.set_title('Comparing Growth Rates')
ax.legend()
ax.grid(True, alpha=0.3)

plt.show()
```

**Line style options:**
- `'-'` or `'solid'`: Solid line
- `'--'` or `'dashed'`: Dashed line
- `'-.'` or `'dashdot'`: Dash-dot line
- `':'` or `'dotted'`: Dotted line

### Scatter Plots

Scatter plots show the relationship between two variables:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

# Generate sample data
np.random.seed(42)
x = np.random.randn(100)
y = 2 * x + np.random.randn(100) * 0.5
colors = np.random.rand(100)
sizes = np.abs(np.random.randn(100)) * 100

# Create scatter plot with variable colors and sizes
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')

ax.set_xlabel('X Variable')
ax.set_ylabel('Y Variable')
ax.set_title('Scatter Plot with Color and Size Encoding')

# Add colorbar
plt.colorbar(scatter, ax=ax, label='Color Value')

plt.show()
```

### Bar Charts

Bar charts compare quantities across categories:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

categories = ['Product A', 'Product B', 'Product C', 'Product D']
values = [45, 62, 38, 71]
colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6']

bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)

# Add value labels on bars
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            str(value), ha='center', va='bottom', fontweight='bold')

ax.set_xlabel('Products')
ax.set_ylabel('Sales (units)')
ax.set_title('Q4 Sales by Product')
ax.set_ylim(0, 80)

plt.show()
```

### Grouped Bar Charts

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 6))

categories = ['Q1', 'Q2', 'Q3', 'Q4']
product_a = [23, 45, 56, 78]
product_b = [34, 56, 45, 89]
product_c = [45, 34, 67, 56]

x = np.arange(len(categories))
width = 0.25

bars1 = ax.bar(x - width, product_a, width, label='Product A', color='#3498db')
bars2 = ax.bar(x, product_b, width, label='Product B', color='#e74c3c')
bars3 = ax.bar(x + width, product_c, width, label='Product C', color='#2ecc71')

ax.set_xlabel('Quarter')
ax.set_ylabel('Sales (units)')
ax.set_title('Quarterly Sales by Product')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

plt.tight_layout()
plt.show()
```

### Histograms

Histograms show the distribution of a single variable:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

# Generate sample data
np.random.seed(42)
data = np.random.normal(100, 15, 1000)

# Create histogram
n, bins, patches = ax.hist(data, bins=30, color='steelblue',
                            edgecolor='white', alpha=0.7)

# Add mean line
mean_val = np.mean(data)
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2,
           label=f'Mean: {mean_val:.1f}')

ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Test Scores')
ax.legend()

plt.show()
```

### Box Plots

Box plots summarize distributions and highlight outliers:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

# Generate sample data for multiple groups
np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in range(1, 5)]

box = ax.boxplot(data, patch_artist=True, labels=['Group A', 'Group B', 'Group C', 'Group D'])

# Customize colors
colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Groups')
ax.set_ylabel('Values')
ax.set_title('Distribution Comparison Across Groups')
ax.grid(True, axis='y', alpha=0.3)

plt.show()
```

## Subplots and Multiple Axes

### Creating Multiple Subplots

```python
import matplotlib.pyplot as plt
import numpy as np

# Create a 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

x = np.linspace(0, 10, 100)

# Top-left: Line plot
axes[0, 0].plot(x, np.sin(x), color='blue')
axes[0, 0].set_title('Sine Wave')

# Top-right: Scatter plot
axes[0, 1].scatter(np.random.rand(50), np.random.rand(50), alpha=0.6)
axes[0, 1].set_title('Random Scatter')

# Bottom-left: Bar chart
axes[1, 0].bar(['A', 'B', 'C', 'D'], [3, 7, 2, 5], color='green')
axes[1, 0].set_title('Bar Chart')

# Bottom-right: Histogram
axes[1, 1].hist(np.random.randn(1000), bins=30, color='purple', alpha=0.7)
axes[1, 1].set_title('Histogram')

plt.tight_layout()
plt.show()
```

### Sharing Axes

```python
import matplotlib.pyplot as plt
import numpy as np

# Share x-axis across all subplots in a column
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

x = np.linspace(0, 10, 100)

axes[0].plot(x, np.sin(x))
axes[0].set_ylabel('sin(x)')

axes[1].plot(x, np.cos(x))
axes[1].set_ylabel('cos(x)')

axes[2].plot(x, np.tan(x))
axes[2].set_ylabel('tan(x)')
axes[2].set_ylim(-5, 5)
axes[2].set_xlabel('x')

fig.suptitle('Trigonometric Functions', fontsize=14)
plt.tight_layout()
plt.show()
```

### GridSpec for Complex Layouts

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(2, 3, figure=fig)

# Large plot spanning two columns
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(np.random.randn(100).cumsum())
ax1.set_title('Time Series (spans 2 columns)')

# Small plot in top-right
ax2 = fig.add_subplot(gs[0, 2])
ax2.bar(['A', 'B', 'C'], [3, 5, 2])
ax2.set_title('Bar Chart')

# Three plots in bottom row
ax3 = fig.add_subplot(gs[1, 0])
ax3.scatter(np.random.rand(30), np.random.rand(30))
ax3.set_title('Scatter')

ax4 = fig.add_subplot(gs[1, 1])
ax4.hist(np.random.randn(100), bins=20)
ax4.set_title('Histogram')

ax5 = fig.add_subplot(gs[1, 2])
ax5.pie([30, 40, 30], labels=['X', 'Y', 'Z'], autopct='%1.0f%%')
ax5.set_title('Pie Chart')

plt.tight_layout()
plt.show()
```

## Customization

### Colors

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

x = np.linspace(0, 10, 100)

# Named colors
axes[0].plot(x, np.sin(x), color='steelblue', linewidth=2)
axes[0].plot(x, np.cos(x), color='coral', linewidth=2)
axes[0].set_title('Named Colors')

# Hex colors
axes[1].plot(x, np.sin(x), color='#1abc9c', linewidth=2)
axes[1].plot(x, np.cos(x), color='#e74c3c', linewidth=2)
axes[1].set_title('Hex Colors')

# RGB tuples (values 0-1)
axes[2].plot(x, np.sin(x), color=(0.2, 0.4, 0.6), linewidth=2)
axes[2].plot(x, np.cos(x), color=(0.8, 0.3, 0.3), linewidth=2)
axes[2].set_title('RGB Tuples')

plt.tight_layout()
plt.show()
```

### Fonts and Text

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=2)

# Title with custom font properties
ax.set_title('Customized Text Styling', fontsize=18, fontweight='bold',
             fontfamily='serif', color='navy')

# Axis labels
ax.set_xlabel('X Axis Label', fontsize=14, fontstyle='italic')
ax.set_ylabel('Y Axis Label', fontsize=14, fontstyle='italic')

# Add annotation
ax.annotate('Peak', xy=(np.pi/2, 1), xytext=(np.pi/2 + 1, 1.3),
            fontsize=12, arrowprops=dict(arrowstyle='->', color='red'),
            color='red')

# Add text box
textstr = 'Sample Text\nBox'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)

plt.show()
```

### Ticks and Spines

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

x = np.linspace(0, 10, 100)

# Default ticks
axes[0].plot(x, np.sin(x))
axes[0].set_title('Default Styling')

# Customized ticks and spines
axes[1].plot(x, np.sin(x))
axes[1].set_title('Customized Ticks and Spines')

# Customize ticks
axes[1].set_xticks([0, np.pi, 2*np.pi, 3*np.pi])
axes[1].set_xticklabels(['0', '$\pi$', '$2\pi$', '$3\pi$'])
axes[1].tick_params(axis='both', which='major', labelsize=12,
                    direction='in', length=6)

# Remove top and right spines
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

# Customize remaining spines
axes[1].spines['bottom'].set_linewidth(1.5)
axes[1].spines['left'].set_linewidth(1.5)

plt.tight_layout()
plt.show()
```

### Legends

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)

ax.plot(x, np.sin(x), label='Sine', linewidth=2)
ax.plot(x, np.cos(x), label='Cosine', linewidth=2)
ax.plot(x, np.sin(x) + np.cos(x), label='Sum', linewidth=2)

# Customized legend
ax.legend(
    loc='upper right',           # Location
    fontsize=12,                 # Font size
    frameon=True,                # Show frame
    fancybox=True,               # Rounded corners
    shadow=True,                 # Shadow effect
    ncol=1,                      # Number of columns
    title='Functions',           # Legend title
    title_fontsize=14            # Title font size
)

ax.set_title('Legend Customization')
plt.show()
```

## Saving Figures

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(np.random.randn(100).cumsum())
ax.set_title('Random Walk')

# Save as PNG with high resolution
fig.savefig('plot.png', dpi=300, bbox_inches='tight')

# Save as PDF (vector format, ideal for publications)
fig.savefig('plot.pdf', bbox_inches='tight')

# Save as SVG (vector format, ideal for web)
fig.savefig('plot.svg', bbox_inches='tight')

# Save with transparent background
fig.savefig('plot_transparent.png', dpi=300, transparent=True, bbox_inches='tight')
```

**Key parameters:**
- `dpi`: Dots per inch (resolution for raster formats)
- `bbox_inches='tight'`: Removes excess whitespace
- `transparent`: Transparent background
- `facecolor`: Background color

## Styles and Themes

```python
import matplotlib.pyplot as plt
import numpy as np

# View available styles
print(plt.style.available)

# Use a built-in style
plt.style.use('seaborn-v0_8-whitegrid')

fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')
ax.legend()
ax.set_title('Using seaborn-whitegrid Style')
plt.show()

# Reset to default
plt.style.use('default')
```

**Popular built-in styles:**
- `'seaborn-v0_8-whitegrid'`: Clean with white grid
- `'seaborn-v0_8-darkgrid'`: Clean with dark grid
- `'ggplot'`: R's ggplot2 style
- `'fivethirtyeight'`: FiveThirtyEight blog style
- `'bmh'`: Bayesian Methods for Hackers style

### Creating Custom Styles

```python
import matplotlib.pyplot as plt

# Customize rcParams
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 100,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'lines.linewidth': 2,
    'lines.markersize': 8,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'sans-serif',
})
```

## Summary

Matplotlib provides complete control over every aspect of a visualization:

| Concept | Description |
|---------|-------------|
| Figure | The overall container for the plot |
| Axes | Individual plot area within a figure |
| pyplot | Simple state-based interface |
| Object-Oriented | Explicit control via fig, ax objects |
| Subplots | Multiple plots in one figure |
| Customization | Colors, fonts, ticks, spines, legends |
| Saving | PNG, PDF, SVG with various options |
| Styles | Pre-built themes for consistent styling |

## Further Reading

- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
