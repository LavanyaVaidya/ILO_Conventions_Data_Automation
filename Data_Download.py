import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://normlex.ilo.org/dyn/nrmlx_en/f?p=1000:10011::::10011:P10011_DISPLAY_BY,P10011_CONVENTION_TYPE_CODE:1,F"

# Download page
response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Find the table
table = soup.find("table", class_="grid")

if table is None:
    raise Exception("Table with class='grid' not found")

rows = table.find_all("tr")

# ---------------------------
# Build column names
# ---------------------------

header1 = rows[0].find_all(["td", "th"])
header2 = rows[1].find_all(["td", "th"])

columns = ["Country"]

groups = []

# Skip Country column
for cell in header1[1:]:
    group = cell.get_text(" ", strip=True)
    colspan = int(cell.get("colspan", 1))

    groups.extend([group] * colspan)

codes = [
    cell.get_text(strip=True)
    for cell in header2[1:]
]

for group, code in zip(groups, codes):
    group = (
        group.replace(" ", "_")
             .replace("-", "_")
             .replace("/", "_")
    )

    columns.append(f"{group}_{code}")

# ---------------------------
# Read data rows
# ---------------------------

data = []

for tr in rows[2:]:

    if "note" in tr.get("class", []):
        continue

    tds = tr.find_all("td")

    if not tds:
        continue

    row = []

    # Country
    row.append(
        tds[0].get_text(" ", strip=True)
    )

    # Remaining values
    for td in tds[1:]:

        year = td.find("span", class_="show_year")
        no_value = td.find("span", class_="noValue")

        if year:
            row.append(year.get_text(strip=True))
        elif no_value:
            row.append(None)
        else:
            row.append(None)

    data.append(row)

# ---------------------------
# DataFrame
# ---------------------------

df = pd.DataFrame(data, columns=columns)

print(df.head())

df.to_csv(
    "fundamental_conventions.csv",
    index=False
)

print("Saved to fundamental_conventions.csv")