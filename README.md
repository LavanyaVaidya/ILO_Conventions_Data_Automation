# ILO_Conventions_Data_Automation# ILO Normlex Ratification Scraper

This project scrapes the latest ILO ratifications from the Normlex website.

## Workflow

1. Open the Normlex homepage.
2. Find the **Latest Ratifications** section.
3. Read the latest month's ratifications.
4. Extract all ILO convention/protocol codes.
5. Check whether any of the ratified codes belong to the 11 Fundamental Conventions.
6. If none are found, the script exits.
7. If one or more Fundamental Conventions are found:

   * Locate the **Ratification comparative data** section.
   * Open the **Fundamental Conventions** comparative table.
   * Scrape the entire table.
   * Generate a wide-format CSV.
   * Add the latest ratification date as the `business_date` column (format: `dd-mm-yyyy`).

---

# Prerequisites

* Python 3.10 or later (Python 3.11 recommended)
* Internet connection

Verify your Python installation:

```bash
python --version
```

or

```bash
python3 --version
```

---

# Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

---

# Create a virtual environment (Recommended)

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

# Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the scraper

```bash
python main.py
```

Replace `main.py` with the actual entry-point script if it has a different name.

---

# Output

When a Fundamental Convention is ratified during the latest reporting month, the script generates a CSV containing:

* Country
* Ratification year for each Fundamental Convention/Protocol
* business_date (dd-mm-yyyy)

Example:

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
business_date
```

If no Fundamental Convention is ratified in the latest month, the script exits without generating a CSV.

---

# Updating dependencies

If additional libraries are added in the future, update the requirements file:

```bash
pip freeze > requirements.txt
```
