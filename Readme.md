# Electric Vehicle Market Penetration and Growth Forecasting in Washington State

A Python project analyzing EV registration data in Washington State to visualize market trends, forecast future growth, and evaluate distribution by geography, vehicle type, and range.

## Features
- Loads and cleans EV registration data, displaying dataset info and handling missing values.
- Visualizes EV market trends with high-quality matplotlib plots (150 DPI):
  - EV adoption over time (bar plot).
  - Top 5 cities in top counties by registrations (bar plot with county hue).
  - Distribution of electric vehicle types (bar plot).
  - Top 5 popular EV makes (bar plot).
  - Top 5 models in top 3 makes (bar plot with make hue).
  - Average electric range by model year (line plot).
  - Top 5 models by average range in top makes (bar plot with make hue).
  - Current and forecasted EV market (line plot with actual vs. forecast).
- Ensures proper layout with visible legends and labels using adjusted padding.
- Forecasts EV registrations for 2024–2029 using exponential growth.
- Optimized for performance: streamlined data processing, reduced runtime by ~80%, and minimized memory usage.
- Compatible with future pandas versions: fixed dtype warnings.

## Setup
1. **Prerequisites**:
   - Python 3.8 or later
   - Install dependencies: `pip install -r requirements.txt`

2. **Project Structure**:
   EV-Market-Analysis/
   ├── scripts/
   │   ├── data_processor.py
   ├── input/
   │   ├── ev_data.csv
   ├── output/
   │   ├── ev_data_ev_adoption_over_time_*.png
   │   ├── ev_data_top_cities_in_top_counties_*.png
   │   ├── ev_data_ev_type_distribution_*.png
   │   ├── ev_data_top_5_makes_*.png
   │   ├── ev_data_top_models_in_top_makes_*.png
   │   ├── ev_data_average_range_by_year_*.png
   │   ├── ev_data_top_models_by_range_*.png
   │   ├── ev_data_ev_market_forecast_*.png
   ├── logs/
   ├── requirements.txt
   ├── README.md



3. **Usage**:
- Clone the repository: `git clone https://github.com/yourusername/EV-Market-Analysis.git`
- Install dependencies: `pip install -r requirements.txt`
- Run the script: `python scripts/data_processor.py`
- Check the `output` folder for updated plots (`*.png`).

## Example
- Input: `input/ev_data.csv` (177,477 rows after filtering, including columns like `Model Year`, `Make`, `Electric Range`)
- Outputs:
  - Console: Dataset preview, info, missing values, and forecasted registrations (2024–2029).
  - Plots in `output`:
 - `ev_data_ev_adoption_over_time_*.png`
 - `ev_data_top_cities_in_top_counties_*.png`
 - `ev_data_ev_type_distribution_*.png`
 - `ev_data_top_5_makes_*.png`
 - `ev_data_top_models_in_top_makes_*.png`
 - `ev_data_average_range_by_year_*.png`
 - `ev_data_top_models_by_range_*.png`
 - `ev_data_ev_market_forecast_*.png`
  - No log file (logging to console only).

## Insights
- Forecasted EV registrations in WA grow exponentially, reaching ~627,171 by 2029.
- High adoption in counties like King and cities like Seattle suggests targeted infrastructure investment.

## About
This project was developed as part of my portfolio to demonstrate data analysis, forecasting, and visualization skills.
Check out my [GitHub profile](https://github.com/ganeshpadavala) or connect with me on [LinkedIn](https://www.linkedin.com/in/ganesh-padavala-b84959204/)