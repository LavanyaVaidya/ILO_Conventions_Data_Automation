# ILO Normlex Fundamental Convention Scraper

## Overview

This project automates the extraction of the latest ratification data for the ILO Fundamental Conventions from the Normlex website.

The scraper first checks whether any Fundamental Convention has been ratified in the latest month's ratifications. It only downloads the comparative ratification table when required, avoiding unnecessary processing.

---

## Project Structure

```
.
├── main.py                 # Entry point
├── homepage.py             # Homepage parser
├── fundamental.py          # Fundamental convention table parser
├── config.py               # URLs and constants
├── requirements.txt
├── .gitignore
└── output/
    └── fundamental_conventions.csv
```

---

## Workflow

The scraper performs the following steps:

1. Opens the Normlex homepage.
2. Finds the **Latest Ratifications** section.
3. Reads the latest month's ratifications.
4. Extracts all ratified convention/protocol codes.
5. Checks whether any of the ratifications belong to the Fundamental Conventions.
6. If none are found, the script exits.
7. Otherwise:

   * Finds the **Ratification comparative data** section.
   * Opens the **Fundamental Conventions** comparative table.
   * Downloads the complete country-wise ratification table.
   * Creates a CSV in wide format.
   * Adds the latest ratification date as the `BUSINESS_DATE` column.

---

## Output

Example output:

```
Country,
Freedom_of_association_C087,
Freedom_of_association_C098,
Forced_labour_C029,
Forced_labour_P029,
Forced_labour_C105,
Discrimination_C100,
Discrimination_C111,
Child_labour_C138,
Child_labour_C182,
Occupational_safety_and_health_C155,
Occupational_safety_and_health_C187,
BUSINESS_DATE
```

`BUSINESS_DATE` is stored in the format:

```
dd-mm-yyyy
```

Example:

```
04-06-2026
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

### 2. Create a virtual environment (Recommended)

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the scraper

Run the following command:

```bash
python main.py
```

---

## Generated Output

If a Fundamental Convention has been ratified in the latest reporting month, the scraper generates:

```
fundamental_conventions.csv
```

If no Fundamental Convention has been ratified, the script exits after displaying an informational message.

---

## Configuration

All configurable values are maintained in `config.py`.

Current configuration includes:

* Normlex homepage URL
* Fundamental Convention codes

Additional datasets can be added by extending this file.

---

## Extending the Project

The project has been designed to support additional ILO datasets.

To add another dataset:

1. Create a new parser module (for example `governance.py`).
2. Add any required configuration to `config.py`.
3. Import the new parser into `main.py`.
4. Invoke it when the corresponding conditions are met.

This modular structure keeps each scraper independent and makes future maintenance easier.

---

## Dependencies

* requests
* beautifulsoup4
* pandas
* lxml

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Notes

* The scraper navigates through the website using the homepage instead of hardcoded report URLs wherever possible.
* Report links are discovered dynamically from the homepage, making the scraper more resilient to changes in internal page identifiers.
* The comparative report is downloaded only when a newly ratified Fundamental Convention is detected.
