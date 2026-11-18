# COVID-19 Data Analysis and Visualization
# Student Final Project

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Dataset source: Our World in Data
DATA_URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"

# Countries selected for comparison
COUNTRIES = ["India", "United States", "Brazil", "United Kingdom", "Germany"]

# Project folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
GRAPH_DIR = os.path.join(OUTPUT_DIR, "graphs")

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)


def load_covid_data():
    """Download the public dataset and prepare the required columns."""
    print("\nDownloading COVID-19 dataset...")
    try:
        data = pd.read_csv(DATA_URL, low_memory=False)
    except Exception as error:
        print("Dataset download failed.")
        print("Please check your internet connection and try again.")
        print("Error:", error)
        return None

    required_columns = ["location", "date"]
    for column in required_columns:
        if column not in data.columns:
            print("Required column is missing:", column)
            return None

    optional_columns = [
        "total_cases", "new_cases", "total_deaths", "new_deaths",
        "stringency_index", "new_vaccinations", "total_recovered"
    ]

    for column in optional_columns:
        if column not in data.columns:
            data[column] = np.nan

    selected_columns = required_columns + optional_columns
    data = data[selected_columns].copy()

    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    numeric_columns = optional_columns
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(subset=["location", "date"])
    data = data[data["location"].isin(COUNTRIES)].copy()
    data = data.sort_values(["location", "date"])

    if data.empty:
        print("No records found for the selected countries.")
        return None

    # Save the cleaned dataset for future reference.
    cleaned_file = os.path.join(DATASET_DIR, "covid_data.csv")
    data.to_csv(cleaned_file, index=False)

    print("Dataset downloaded and cleaned successfully.")
    print("Total records:", len(data))
    print("Countries found:", ", ".join(sorted(data["location"].unique())))
    return data


def show_basic_information(data):
    """Display basic information about the dataset."""
    print("\n========== DATASET INFORMATION ==========")
    print("Number of rows:", data.shape[0])
    print("Number of columns:", data.shape[1])
    print("\nFirst five records:")
    print(data.head())
    print("\nMissing values:")
    print(data.isnull().sum())


def create_country_summary(data):
    """Create a country-wise summary using the latest available record."""
    summary = (
        data.sort_values("date")
        .groupby("location", as_index=False)
        .tail(1)
        [["location", "date", "total_cases", "total_deaths"]]
        .copy()
    )

    summary = summary.rename(columns={
        "location": "Country",
        "date": "Latest Date",
        "total_cases": "Total Cases",
        "total_deaths": "Total Deaths"
    })

    summary["Total Cases"] = summary["Total Cases"].round(0)
    summary["Total Deaths"] = summary["Total Deaths"].round(0)

    summary_file = os.path.join(OUTPUT_DIR, "country_summary.csv")
    summary.to_csv(summary_file, index=False)

    print("\n========== COUNTRY-WISE SUMMARY ==========")
    print(summary.to_string(index=False))
    return summary


def plot_monthly_cases(data):
    """Compare monthly new COVID-19 cases across selected countries."""
    monthly = data.copy()
    monthly["Month"] = monthly["date"].dt.to_period("M").dt.to_timestamp()
    monthly = monthly.groupby(["Month", "location"], as_index=False)["new_cases"].sum()

    plt.figure(figsize=(13, 6))
    sns.lineplot(data=monthly, x="Month", y="new_cases", hue="location")
    plt.title("Monthly New COVID-19 Cases by Country")
    plt.xlabel("Month")
    plt.ylabel("New Cases")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "monthly_cases_comparison.png"))
    plt.close()


def plot_total_deaths(summary):
    """Show latest reported total deaths for selected countries."""
    chart_data = summary.dropna(subset=["Total Deaths"]).copy()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=chart_data, x="Country", y="Total Deaths")
    plt.title("Total COVID-19 Deaths by Country")
    plt.xlabel("Country")
    plt.ylabel("Total Deaths")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "total_deaths_by_country.png"))
    plt.close()


def plot_india_daily_cases(data):
    """Show daily and seven-day average cases for India."""
    india = data[data["location"] == "India"].copy()

    if india.empty:
        print("India data is not available. Daily cases graph skipped.")
        return

    india = india.sort_values("date")
    india["7_Day_Average"] = india["new_cases"].rolling(
        window=7, min_periods=1
    ).mean()

    plt.figure(figsize=(13, 6))
    plt.plot(india["date"], india["new_cases"], label="Daily New Cases", alpha=0.5)
    plt.plot(india["date"], india["7_Day_Average"], label="7-Day Average")
    plt.title("Daily COVID-19 Cases in India")
    plt.xlabel("Date")
    plt.ylabel("New Cases")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "india_daily_cases.png"))
    plt.close()


def plot_government_stringency(data):
    """Compare monthly stringency index and cases for India."""
    india = data[data["location"] == "India"].copy()
    india = india.dropna(subset=["stringency_index", "new_cases"])

    if india.empty:
        print("Stringency Index data is unavailable. Policy graph skipped.")
        return

    india["Month"] = india["date"].dt.to_period("M").dt.to_timestamp()
    monthly = india.groupby("Month", as_index=False).agg({
        "stringency_index": "mean",
        "new_cases": "sum"
    })

    fig, axis1 = plt.subplots(figsize=(13, 6))
    axis1.plot(
        monthly["Month"], monthly["stringency_index"],
        label="Average Stringency Index"
    )
    axis1.set_xlabel("Month")
    axis1.set_ylabel("Stringency Index")

    axis2 = axis1.twinx()
    axis2.plot(
        monthly["Month"], monthly["new_cases"],
        label="Monthly New Cases", linestyle="--"
    )
    axis2.set_ylabel("Monthly New Cases")

    plt.title("Government Stringency Index and COVID-19 Cases in India")
    fig.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "india_stringency_vs_cases.png"))
    plt.close()


def plot_recoveries_if_available(data):
    """Plot recovery data only if the source contains a recovery column."""
    recovery_data = data.dropna(subset=["total_recovered"])

    if recovery_data.empty:
        print("\nRecovery analysis skipped: the selected OWID dataset")
        print("does not provide usable total_recovered values for these countries.")
        return

    latest = (
        recovery_data.sort_values("date")
        .groupby("location", as_index=False)
        .tail(1)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=latest, x="location", y="total_recovered")
    plt.title("Latest Available Total Recoveries by Country")
    plt.xlabel("Country")
    plt.ylabel("Total Recoveries")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "total_recoveries_by_country.png"))
    plt.close()


def save_project_summary(data, summary):
    """Save a short text report with results calculated from the dataset."""
    lines = [
        "COVID-19 DATA ANALYSIS AND VISUALIZATION",
        "=" * 45,
        f"Records analysed: {len(data)}",
        f"Countries analysed: {', '.join(sorted(data['location'].unique()))}",
        f"Date range: {data['date'].min().date()} to {data['date'].max().date()}",
        "",
        "Latest available country-wise totals:",
        summary.to_string(index=False),
        "",
        "Note: COVID-19 reporting methods and coverage differ by country and date.",
        "Stringency Index is a policy measure, not proof of cause and effect."
    ]

    report_file = os.path.join(OUTPUT_DIR, "analysis_summary.txt")
    with open(report_file, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def main():
    print("==============================================")
    print(" COVID-19 DATA ANALYSIS AND VISUALIZATION")
    print("==============================================")

    data = load_covid_data()
    if data is None:
        return

    show_basic_information(data)
    summary = create_country_summary(data)

    print("\nCreating graphs...")
    plot_monthly_cases(data)
    plot_total_deaths(summary)
    plot_india_daily_cases(data)
    plot_government_stringency(data)
    plot_recoveries_if_available(data)

    save_project_summary(data, summary)

    print("\nProject completed successfully!")
    print("Cleaned dataset: dataset/covid_data.csv")
    print("Country summary: output/country_summary.csv")
    print("Text report: output/analysis_summary.txt")
    print("Graphs are saved in: output/graphs/")


if __name__ == "__main__":
    main()