# COVID-19 Data Analysis and Visualization

## 1. Introduction
COVID-19 is a disease caused by the coronavirus SARS-CoV-2. This project analyses publicly available COVID-19 data for selected countries and presents the results using graphs.

## 2. Objectives
- Study COVID-19 cases and deaths over time.
- Compare reported cases and deaths across countries.
- Study daily and monthly case trends.
- Explore the relationship between government response stringency and reported cases.
- Present the analysis using clear visualizations.

## 3. Technologies Used
- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- VS Code

## 4. Dataset
The project downloads the compact COVID-19 dataset from Our World in Data (OWID).

Dataset URL:
https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv

Documentation:
https://docs.owid.io/projects/etl/api/covid/

The program selects India, United States, Brazil, United Kingdom and Germany when records are available. It saves the cleaned selected records to `dataset/covid_data.csv`.

## 5. Project Folder Structure
```text
COVID19_Data_Analysis_Project/
|
|-- dataset/
|   |-- covid_data.csv          (created after running the program)
|
|-- output/
|   |-- graphs/
|   |   |-- monthly_cases_comparison.png
|   |   |-- total_deaths_by_country.png
|   |   |-- india_daily_cases.png
|   |   |-- india_stringency_vs_cases.png
|   |   |-- total_recoveries_by_country.png (only if data is available)
|   |
|   |-- country_summary.csv
|   |-- analysis_summary.txt
|
|-- main.py
|-- README.md
|-- requirements.txt
```

## 6. Installation
Open the project folder in VS Code.

Open the terminal and run:

```bash
python -m pip install -r requirements.txt
```

## 7. How to Run
Run this command in the VS Code terminal:

```bash
python main.py
```

An internet connection is required because the program downloads the dataset when it runs.

## 8. Analysis Performed
1. Dataset information and missing-value check.
2. Latest available total cases and deaths by selected country.
3. Monthly new-case comparison.
4. Country-wise total-death bar chart.
5. India's daily new cases and seven-day average.
6. India's monthly Stringency Index compared with monthly new cases.
7. Recovery chart only if usable recovery data is present in the downloaded dataset.

## 9. Output
After successful execution:
- The cleaned dataset is saved in `dataset/covid_data.csv`.
- Country-wise results are saved in `output/country_summary.csv`.
- A text report is saved in `output/analysis_summary.txt`.
- Graphs are saved in `output/graphs/`.

The exact numbers depend on the dataset version downloaded when the program is run. The console and output files show the actual calculated results; no fixed sample totals are assumed.

## 10. Conclusion
This project demonstrates how Python libraries can be used to collect, clean, analyse and visualize public health data. The graphs help compare reported COVID-19 trends across selected countries and examine how government response stringency changed over time.

The Stringency Index is a measure of government policy responses. A comparison with case counts does not prove that a policy caused cases to rise or fall. Reporting methods, testing, population, timing and other factors can also affect the data.

## 11. Limitations
- Countries may report cases and deaths differently.
- Some dates and indicators may contain missing values.
- Recovery data is not consistently available in the selected global dataset. The program does not invent missing recovery figures.
- The dataset may be revised by its provider.

## 12. Data Source and Credit
Data source: Our World in Data (OWID), COVID-19 dataset.

Please credit Our World in Data and review its dataset documentation and licensing information when presenting or sharing this project.

- Dataset: https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv
- Documentation: https://docs.owid.io/projects/etl/api/covid/
