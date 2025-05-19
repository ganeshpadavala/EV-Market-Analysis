import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import gc

def setup_logging():
    """Set up logging to console only."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def load_data(file_path):
    """Load CSV file into a pandas DataFrame with optimized settings."""
    usecols = ['State', 'Model Year', 'Make', 'Model', 'County', 'City', 'Electric Vehicle Type', 'Electric Range']
    dtypes = {
        'State': 'category',
        'Model Year': 'int16',
        'Make': 'category',
        'Model': 'category',
        'County': 'category',
        'City': 'category',
        'Electric Vehicle Type': 'category',
        'Electric Range': 'float32'
    }
    try:
        df = pd.read_csv(file_path, usecols=usecols, dtype=dtypes)
        logging.info(f"Loaded data from {file_path} with {len(df)} rows and {len(df.columns)} columns")
        print("Dataset Preview:")
        print(df.head())
        print("\nDataset Info:")
        df.info()
        print("\nMissing Values:")
        print(df.isnull().sum())
        df = df.dropna().reset_index(drop=True)
        logging.info(f"Dropped missing values, remaining rows: {len(df)}")
        df = df[df['State'] == 'WA'].reset_index(drop=True)
        logging.info(f"Filtered data for WA state: {len(df)} rows")
        return df
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        return None

def plot_all_charts(df, forecasted_evs, output_prefix):
    """Plot charts with matplotlib styling, optimizing memory and time."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Precompute aggregations to reuse
    ev_adoption_by_year = df['Model Year'].value_counts().sort_index()
    ev_county_distribution = df['County'].value_counts()
    top_counties = ev_county_distribution.head(3).index
    top_counties_data = df[df['County'].isin(top_counties)]
    ev_type_distribution = df['Electric Vehicle Type'].value_counts()
    ev_make_distribution = df['Make'].value_counts().head(5)
    top_3_makes = ev_make_distribution.head(3).index
    top_makes_data = df[df['Make'].isin(top_3_makes)]

    # EV Adoption Over Time
    fig, ax = plt.subplots(figsize=(8, 4))
    years = ev_adoption_by_year.index.astype(int)
    ax.bar(years, ev_adoption_by_year.values, color=plt.cm.viridis(np.linspace(0, 1, len(years))))
    ax.set_title('EV Adoption Over Time')
    ax.set_xlabel('Model Year')
    ax.set_ylabel('Number of Vehicles')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)  # Add padding for rotated x-axis labels
    filename = f'{output_prefix}_ev_adoption_over_time_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved EV adoption over time plot")

    # Top Cities in Top Counties
    fig, ax = plt.subplots(figsize=(8, 6))
    ev_city_distribution_top_counties = top_counties_data.groupby(['County', 'City'], observed=True).size().sort_values(ascending=False).head(5).reset_index(name='Number of Vehicles')
    ev_city_distribution_top_counties['City'] = ev_city_distribution_top_counties['City'].astype(str).apply(lambda x: x[:12] + '...' if len(x) > 12 else x)
    colors = plt.cm.magma(np.linspace(0, 1, len(top_counties)))
    for i, county in enumerate(ev_city_distribution_top_counties['County'].unique()):
        subset = ev_city_distribution_top_counties[ev_city_distribution_top_counties['County'] == county]
        ax.barh(subset['City'], subset['Number of Vehicles'], color=colors[i], label=county)
    ax.set_title('Top Cities in Top Counties by EV Registrations')
    ax.set_xlabel('Number of Vehicles')
    ax.set_ylabel('City')
    ax.legend(title='County', loc='upper right')  # Legend inside, top-right
    filename = f'{output_prefix}_top_cities_in_top_counties_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved top cities in top counties plot")

    # EV Type Distribution
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(ev_type_distribution.index, ev_type_distribution.values, color=plt.cm.magma(np.linspace(0, 1, len(ev_type_distribution))))
    ax.set_title('Distribution of Electric Vehicle Types')
    ax.set_xlabel('Number of Vehicles')
    ax.set_ylabel('Electric Vehicle Type')
    filename = f'{output_prefix}_ev_type_distribution_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved EV type distribution plot")

    # Top 5 Makes
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(ev_make_distribution.index, ev_make_distribution.values, color=plt.cm.cubehelix(np.linspace(0, 1, len(ev_make_distribution))))
    ax.set_title('Top 5 Popular EV Makes')
    ax.set_xlabel('Number of Vehicles')
    ax.set_ylabel('Make')
    filename = f'{output_prefix}_top_5_makes_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved top 5 makes plot")

    # Top Models in Top 3 Makes
    fig, ax = plt.subplots(figsize=(8, 6))
    ev_model_distribution_top_makes = top_makes_data.groupby(['Make', 'Model'], observed=True).size().sort_values(ascending=False).reset_index(name='Number of Vehicles')
    top_models = ev_model_distribution_top_makes.head(5).copy()
    top_models['Model'] = top_models['Model'].astype(str).apply(lambda x: x[:12] + '...' if len(x) > 12 else x)
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_3_makes)))
    for i, make in enumerate(top_models['Make'].unique()):
        subset = top_models[top_models['Make'] == make]
        ax.barh(subset['Model'], subset['Number of Vehicles'], color=colors[i], label=make)
    ax.set_title('Top Models in Top 3 Makes by EV Registrations')
    ax.set_xlabel('Number of Vehicles')
    ax.set_ylabel('Model')
    ax.legend(title='Make', loc='upper right')  # Legend inside, top-right
    filename = f'{output_prefix}_top_models_in_top_makes_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved top models in top makes plot")

    # Average Range by Model Year
    fig, ax = plt.subplots(figsize=(8, 4))
    average_range_by_year = df.groupby('Model Year')['Electric Range'].mean().reset_index()
    ax.plot(average_range_by_year['Model Year'], average_range_by_year['Electric Range'], marker='o', color='green')
    ax.set_title('Average Electric Range by Model Year')
    ax.set_xlabel('Model Year')
    ax.set_ylabel('Average Electric Range (miles)')
    filename = f'{output_prefix}_average_range_by_year_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved average range by year plot")

    # Top Models by Average Range
    fig, ax = plt.subplots(figsize=(8, 6))
    average_range_by_model = top_makes_data.groupby(['Make', 'Model'], observed=True)['Electric Range'].mean().sort_values(ascending=False).reset_index()
    top_range_models = average_range_by_model.head(5).copy()
    top_range_models['Model'] = top_range_models['Model'].astype(str).apply(lambda x: x[:12] + '...' if len(x) > 12 else x)
    colors = plt.cm.cool(np.linspace(0, 1, len(top_3_makes)))
    for i, make in enumerate(top_range_models['Make'].unique()):
        subset = top_range_models[top_range_models['Make'] == make]
        ax.barh(subset['Model'], subset['Electric Range'], color=colors[i], label=make)
    ax.set_title('Top 5 Models by Average Range in Top Makes')
    ax.set_xlabel('Average Electric Range (miles)')
    ax.set_ylabel('Model')
    ax.legend(title='Make', loc='upper right')  # Legend inside, top-right
    filename = f'{output_prefix}_top_models_by_range_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved top models by range plot")

    # Forecasted EV Market
    fig, ax = plt.subplots(figsize=(8, 5))
    ev_registration_counts = df['Model Year'].value_counts().sort_index()
    filtered_years = ev_registration_counts[ev_registration_counts.index <= 2023]
    years = np.arange(filtered_years.index.min(), 2029 + 1)
    actual_years = filtered_years.index
    forecast_years_full = np.arange(2024, 2029 + 1)
    actual_values = filtered_years.values
    forecasted_values_full = [forecasted_evs[year] for year in forecast_years_full]
    ax.plot(actual_years, actual_values, 'bo-', label='Actual Registrations')
    ax.plot(forecast_years_full, forecasted_values_full, 'ro--', label='Forecasted Registrations')
    ax.set_title('Current & Estimated EV Market')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of EV Registrations')
    ax.legend(loc='upper left')  # Legend inside, top-left
    filename = f'{output_prefix}_ev_market_forecast_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    gc.collect()
    logging.info(f"Saved EV market forecast plot")

def forecast_future_registrations(df):
    """Forecast future EV registrations using exponential growth."""
    ev_registration_counts = df['Model Year'].value_counts().sort_index()
    filtered_years = ev_registration_counts[ev_registration_counts.index <= 2023]

    def exp_growth(x, a, b):
        return a * np.exp(b * x)

    x_data = filtered_years.index - filtered_years.index.min()
    y_data = filtered_years.values

    params, _ = curve_fit(exp_growth, x_data, y_data)
    forecast_years = np.arange(2024, 2029 + 1) - filtered_years.index.min()
    forecasted_values = exp_growth(forecast_years, *params)
    forecasted_evs = dict(zip(forecast_years + filtered_years.index.min(), forecasted_values))

    return forecasted_evs

def main():
    """Main function to analyze and visualize EV registrations."""
    setup_logging()

    # Get the directory of the script and navigate to the parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level to D:\Python\Project\EV
    input_folder = os.path.join(project_root, 'input')
    output_folder = os.path.join(project_root, 'output')

    # Check if input folder exists
    if not os.path.exists(input_folder):
        logging.error("Input folder does not exist.")
        return

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    filename = 'ev_data.csv'
    file_path = os.path.join(input_folder, filename)
    df = load_data(file_path)

    if df is not None:
        forecasted_evs = forecast_future_registrations(df)
        print("\nForecasted EV Registrations (2024-2029):")
        print(forecasted_evs)
        plot_all_charts(df, forecasted_evs, os.path.join(output_folder, os.path.basename(file_path).split(".")[0]))

if __name__ == "__main__":
    main()