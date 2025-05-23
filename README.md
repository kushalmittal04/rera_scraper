# RERA Odisha Project Scraper

This Python script uses Selenium to scrape real estate project details from the [RERA Odisha website](https://rera.odisha.gov.in/projects/project-list). It collects information like project name, RERA registration number, promoter details, and stores them in a CSV file.

## Features

- Scrapes project name and RERA registration number from the listing page.
- Visits each project's detail page to extract:
  - Promoter name (company)
  - Registered office address
  - GST number
- Saves all data in `rera_projects_data.csv`.

## Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver (must match your Chrome version and be in system PATH)

## Installation

1. Clone this repository or copy the script.
2. Install dependencies:
   ```bash
   pip install selenium
   python main.py
