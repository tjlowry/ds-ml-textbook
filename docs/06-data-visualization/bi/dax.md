# DAX Fundamentals for Data Visualization

## Overview

Data Analysis Expressions (DAX) is a formula language used in Microsoft Power BI, Analysis Services, and Power Pivot for Excel. DAX enables you to create calculated columns, measures, and tables that power interactive visualizations and dashboards. Understanding DAX is essential for building dynamic, data-driven reports.

## DAX Basics

### Calculated Columns vs Measures

**Calculated Columns:**
- Computed row by row at data refresh time
- Stored in the model, increasing file size
- Can be used for filtering and grouping
- Use when you need a value for each row

**Measures:**
- Computed at query time based on filter context
- Not stored, calculated dynamically
- Used for aggregations in visualizations
- Use when you need aggregated results

```dax
// Calculated Column - evaluated for each row
Revenue = Sales[Quantity] * Sales[UnitPrice]

// Measure - aggregated at query time
Total Revenue = SUM(Sales[Revenue])
```

### Basic Syntax

```dax
// Creating a measure
Measure Name = <expression>

// Creating a calculated column (in context of a table)
Column Name = <expression>

// Comments
// This is a single line comment
/* This is a
   multi-line comment */
```

## Aggregation Functions

### Basic Aggregations

```dax
// Sum all values
Total Sales = SUM(Sales[Amount])

// Count rows
Order Count = COUNT(Sales[OrderID])

// Count non-blank values
Customer Count = COUNTA(Customers[CustomerID])

// Count distinct values
Unique Products = DISTINCTCOUNT(Sales[ProductID])

// Average
Average Order Value = AVERAGE(Sales[Amount])

// Minimum and Maximum
First Sale = MIN(Sales[Date])
Last Sale = MAX(Sales[Date])
```

## Iterator Functions

Iterator functions evaluate an expression for each row of a table and then aggregate the results. They are powerful but can be slower on large datasets.

### SUMX Function

`SUMX` is one of the most important DAX functions. It iterates through each row of a table, evaluates an expression, and sums the results.

**Syntax:**

```dax
SUMX(<table>, <expression>)
```

- `<table>`: The table or table expression over which the calculation is performed
- `<expression>`: The DAX expression that returns a number, evaluated for each row

**Example:**

```dax
// Calculate total sales by multiplying quantity by price for each row
Total Sales = SUMX(
    Sales,
    Sales[Quantity] * Sales[UnitPrice]
)
```

This iterates over each row in the `Sales` table, multiplies `Quantity` by `UnitPrice`, and sums all the products.

**When to use SUMX:**
- When you need row-by-row calculations before aggregating
- When the calculation involves multiple columns
- When you need to aggregate over a filtered subset

```dax
// Total sales for products over $100
Premium Product Sales = SUMX(
    FILTER(Sales, Sales[UnitPrice] > 100),
    Sales[Quantity] * Sales[UnitPrice]
)
```

### Other Iterator Functions

```dax
// AVERAGEX - average of row-level calculations
Average Line Total = AVERAGEX(
    Sales,
    Sales[Quantity] * Sales[UnitPrice]
)

// COUNTX - count rows that meet a condition
Large Orders = COUNTX(
    FILTER(Sales, Sales[Amount] > 1000),
    Sales[OrderID]
)

// MAXX and MINX
Largest Order = MAXX(Sales, Sales[Quantity] * Sales[UnitPrice])
Smallest Order = MINX(Sales, Sales[Quantity] * Sales[UnitPrice])

// RANKX - rank values
Product Rank = RANKX(
    ALL(Products),
    [Total Sales],
    ,
    DESC,
    Dense
)
```

### Performance Considerations for Iterators

**Best Practices:**

1. **Minimize use in large models**: Iterators process row by row, which can be slower than column-based aggregations

2. **Use simple expressions**: Keep the expression inside iterators as clear and efficient as possible

3. **Consider calculated columns**: For frequently used row-level calculations, a calculated column might perform better

4. **Filter first, iterate second**: When possible, reduce the row count before iterating

```dax
// Less efficient - iterates all rows, then filters
Inefficient = SUMX(
    Sales,
    IF(Sales[Region] = "West", Sales[Amount], 0)
)

// More efficient - filters first
Efficient = SUMX(
    FILTER(Sales, Sales[Region] = "West"),
    Sales[Amount]
)
```

## Filter Functions

### CALCULATE

`CALCULATE` is the most powerful DAX function. It evaluates an expression in a modified filter context.

```dax
// Basic CALCULATE
Western Sales = CALCULATE(
    SUM(Sales[Amount]),
    Sales[Region] = "West"
)

// Multiple filter conditions (AND logic)
Premium Western Sales = CALCULATE(
    SUM(Sales[Amount]),
    Sales[Region] = "West",
    Products[Category] = "Premium"
)

// Using FILTER for complex conditions
High Value Sales = CALCULATE(
    SUM(Sales[Amount]),
    FILTER(Sales, Sales[Amount] > 1000)
)
```

### ALL, ALLEXCEPT, ALLSELECTED

These functions remove filters from the context:

```dax
// ALL - removes all filters from a table
Percent of Total =
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALL(Sales))
    )

// ALLEXCEPT - removes all filters except specified columns
Category Percent =
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALLEXCEPT(Sales, Sales[Category]))
    )

// ALLSELECTED - respects slicer selections
Selected Percent =
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALLSELECTED(Sales))
    )
```

### FILTER

```dax
// FILTER returns a table with rows that meet the condition
Filtered Sales = CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        Sales,
        Sales[Discount] > 0.1 && Sales[Amount] > 500
    )
)
```

## Time Intelligence

DAX includes powerful functions for time-based calculations.

### Date Table Requirement

Time intelligence requires a proper date table:

```dax
// Create a date table
DateTable =
    ADDCOLUMNS(
        CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31)),
        "Year", YEAR([Date]),
        "Month", MONTH([Date]),
        "MonthName", FORMAT([Date], "MMMM"),
        "Quarter", "Q" & QUARTER([Date]),
        "YearMonth", FORMAT([Date], "YYYY-MM")
    )
```

### Common Time Intelligence Functions

```dax
// Year-to-Date
YTD Sales = TOTALYTD(SUM(Sales[Amount]), DateTable[Date])

// Previous Year
PY Sales = CALCULATE(
    SUM(Sales[Amount]),
    SAMEPERIODLASTYEAR(DateTable[Date])
)

// Year-over-Year Growth
YoY Growth =
    VAR CurrentYear = SUM(Sales[Amount])
    VAR PreviousYear = CALCULATE(
        SUM(Sales[Amount]),
        SAMEPERIODLASTYEAR(DateTable[Date])
    )
    RETURN
        DIVIDE(CurrentYear - PreviousYear, PreviousYear)

// Month-to-Date
MTD Sales = TOTALMTD(SUM(Sales[Amount]), DateTable[Date])

// Previous Month
PM Sales = CALCULATE(
    SUM(Sales[Amount]),
    PREVIOUSMONTH(DateTable[Date])
)

// Rolling 12 Months
Rolling 12M = CALCULATE(
    SUM(Sales[Amount]),
    DATESINPERIOD(DateTable[Date], MAX(DateTable[Date]), -12, MONTH)
)

// Moving Average
3M Moving Avg =
    AVERAGEX(
        DATESINPERIOD(DateTable[Date], MAX(DateTable[Date]), -3, MONTH),
        CALCULATE(SUM(Sales[Amount]))
    )
```

## Variables

Variables improve readability and performance:

```dax
// Without variables (calculates twice)
Profit Margin = DIVIDE(
    SUM(Sales[Revenue]) - SUM(Sales[Cost]),
    SUM(Sales[Revenue])
)

// With variables (calculates once, used twice)
Profit Margin =
    VAR Revenue = SUM(Sales[Revenue])
    VAR Cost = SUM(Sales[Cost])
    VAR Profit = Revenue - Cost
    RETURN
        DIVIDE(Profit, Revenue)
```

## Table Functions

### SUMMARIZE

```dax
// Create a summary table
Sales Summary =
    SUMMARIZE(
        Sales,
        Products[Category],
        "Total Sales", SUM(Sales[Amount]),
        "Order Count", COUNT(Sales[OrderID])
    )
```

### ADDCOLUMNS

```dax
// Add calculated columns to a table
Enhanced Products =
    ADDCOLUMNS(
        Products,
        "Total Sales", CALCULATE(SUM(Sales[Amount])),
        "Avg Price", AVERAGE(Sales[UnitPrice])
    )
```

### UNION, INTERSECT, EXCEPT

```dax
// Combine tables
All Customers =
    UNION(
        Customers2023,
        Customers2024
    )

// Common rows
Repeat Customers =
    INTERSECT(
        VALUES(Sales2023[CustomerID]),
        VALUES(Sales2024[CustomerID])
    )
```

## Measures for Visualizations

### KPI Measures

```dax
// Revenue with formatting
Revenue =
    VAR Rev = SUM(Sales[Amount])
    RETURN
        IF(Rev >= 1000000,
            FORMAT(Rev / 1000000, "$#,##0.0M"),
            FORMAT(Rev, "$#,##0"))

// Status indicator
Sales Status =
    VAR Actual = SUM(Sales[Amount])
    VAR Target = SUM(Targets[Amount])
    RETURN
        SWITCH(
            TRUE(),
            Actual >= Target, "On Track",
            Actual >= Target * 0.9, "At Risk",
            "Behind"
        )

// Traffic light indicator (returns icon)
Status Icon =
    VAR Performance = [Sales vs Target %]
    RETURN
        SWITCH(
            TRUE(),
            Performance >= 1, UNICHAR(128994),    // Green circle
            Performance >= 0.9, UNICHAR(128992),  // Yellow circle
            UNICHAR(128308)                        // Red circle
        )
```

### Conditional Formatting Measures

```dax
// Return color based on performance
Revenue Color =
    VAR Growth = [YoY Growth]
    RETURN
        SWITCH(
            TRUE(),
            Growth > 0.1, "#28a745",   // Green
            Growth > 0, "#ffc107",      // Yellow
            "#dc3545"                   // Red
        )
```

### Dynamic Titles

```dax
// Dynamic chart title
Chart Title =
    VAR SelectedRegion = SELECTEDVALUE(Regions[Region], "All Regions")
    VAR SelectedYear = SELECTEDVALUE(DateTable[Year], "All Years")
    RETURN
        "Sales for " & SelectedRegion & " - " & SelectedYear
```

## Best Practices

### 1. Use Meaningful Names

```dax
// Bad
M1 = SUM(Sales[Amount])

// Good
Total Revenue = SUM(Sales[Amount])
```

### 2. Format for Readability

```dax
// Hard to read
Profit Margin = DIVIDE(SUM(Sales[Revenue])-SUM(Sales[Cost]),SUM(Sales[Revenue]))

// Easy to read
Profit Margin =
    VAR Revenue = SUM(Sales[Revenue])
    VAR Cost = SUM(Sales[Cost])
    VAR Profit = Revenue - Cost
    RETURN
        DIVIDE(Profit, Revenue)
```

### 3. Use DIVIDE Instead of Division Operator

```dax
// Can cause errors with zero denominators
Bad Margin = [Profit] / [Revenue]

// Handles division by zero gracefully
Good Margin = DIVIDE([Profit], [Revenue], 0)
```

### 4. Organize Measures

Group related measures in display folders and use a consistent naming convention:

```
Measures
  |- Revenue
  |    |- Total Revenue
  |    |- YTD Revenue
  |    |- PY Revenue
  |- Costs
  |    |- Total Cost
  |    |- Avg Cost per Unit
  |- Profitability
       |- Gross Profit
       |- Profit Margin %
```

## Summary

| Function Type | Examples | Use Case |
|--------------|----------|----------|
| Aggregation | SUM, COUNT, AVERAGE | Basic totals and counts |
| Iterator | SUMX, AVERAGEX, COUNTX | Row-level calculations |
| Filter | CALCULATE, FILTER, ALL | Modify evaluation context |
| Time Intelligence | TOTALYTD, SAMEPERIODLASTYEAR | Period comparisons |
| Table | SUMMARIZE, ADDCOLUMNS | Create derived tables |

Key takeaways:
- SUMX and other iterators are powerful for row-by-row calculations
- CALCULATE is essential for changing filter context
- Variables improve both readability and performance
- Time intelligence functions require a proper date table
- Measures drive dynamic, interactive visualizations

## Further Reading

- [DAX Guide](https://dax.guide/)
- [SQLBI - DAX Patterns](https://www.daxpatterns.com/)
- [Microsoft DAX Reference](https://docs.microsoft.com/en-us/dax/)
- [The Definitive Guide to DAX](https://www.sqlbi.com/books/the-definitive-guide-to-dax-2nd-edition/)
