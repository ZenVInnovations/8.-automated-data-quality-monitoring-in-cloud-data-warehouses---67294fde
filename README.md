# Data Quality Monitoring Dashboard

This project implements an interactive dashboard for monitoring data quality using Gradio and Great Expectations.

## Features

- Upload CSV files for analysis
- Automatic data quality checks
- Missing value visualization
- Summary statistics
- Detailed validation results

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
python data_quality_dashboard.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://127.0.0.1:7860)

## Usage

1. Click the "Upload CSV File" button to select your data file
2. Click "Analyze Data Quality" to run the analysis
3. View the results in three sections:
   - Summary Statistics: Overview of your data
   - Validation Results: Detailed quality checks
   - Missing Values Visualization: Graph showing missing data patterns

## Data Quality Checks

The dashboard performs the following checks:
- Null value detection for all columns
- Unique value validation for the first column (assumed to be ID)
- Row count validation
- Duplicate row detection

## Requirements

See `requirements.txt` for detailed dependencies. 