
# Sales Dashboard :shopping_trolley:

## Overview

The **Sales Dashboard** is an interactive application built with **Streamlit** that provides visual insights into sales data. The dashboard enables users to analyze sales performance across different regions, years, and vendors. It features multiple graphs and tables, including sales by state, category, and vendor, as well as trends over time. Users can filter data based on regions, years, and specific vendors to explore the sales data in more detail.

## Features

- **Filter Options**: Select the region, year, and vendors to filter the displayed data.
- **Sales Insights**:
  - Visualize **total revenue** and **total sales quantity**.
  - Display **top states** based on sales revenue.
  - Analyze **revenue by product category**.
  - Visualize **monthly revenue trends** over the selected years.
  - View **sales by vendor** and **vendor performance**.
- **Interactive Visualizations**: The dashboard provides interactive graphs and charts using **Plotly**, such as:
  - **Sales by State** (geo map and bar chart)
  - **Revenue by Category** (bar chart)
  - **Monthly Revenue Trend** (line chart)
  - **Vendor Performance** (bar chart)

## Setup

### Prerequisites

Before running the dashboard, you need to install the following dependencies:

1. **Streamlit**: For building the interactive web interface.
2. **Requests**: For fetching sales data from the API.
3. **Pandas**: For data manipulation and analysis.
4. **Plotly**: For creating interactive visualizations.

You can install these dependencies by running:

```bash
pip install streamlit requests pandas plotly
```

This will launch the app in your default web browser.

## Functionality

1. **Filters**: 
   - **Region**: Filter sales data by region or select "Brasil" to view all regions.
   - **Year**: Choose a specific year between 2020 and 2023 or select "Dados de todo o período" to view all years.
   - **Vendors**: Multi-select vendors to filter sales data by specific vendors.

2. **Data Display**:
   - **Revenue by State**: A map and bar chart displaying sales revenue by state.
   - **Revenue by Category**: A bar chart displaying total sales revenue for each product category.
   - **Monthly Revenue**: A line chart showing revenue trends month by month.
   - **Top Vendors**: A bar chart displaying the top vendors based on total sales revenue and number of sales.

3. **Metrics**:
   - **Total Revenue**: Displays the total sales revenue across the selected filters.
   - **Sales Quantity**: Shows the total number of sales for the selected filters.

4. **Customizable Vendor View**: Set the number of top vendors to display based on total revenue or number of sales.


## API Integration

- **Data Source**: The sales data is fetched from the API endpoint `https://labdados.com/produtos`. This endpoint provides sales data in JSON format, which is then processed and visualized in the dashboard.

## Example

After applying the filters, the dashboard will display key performance indicators such as:

- **Total Revenue**: R$ 1,000,000
- **Total Sales Quantity**: 5000 units
- **Revenue by State**: A map showing the sales distribution across Brazilian states.
- **Monthly Revenue Trends**: A line chart showing how sales revenue has changed over the months.
