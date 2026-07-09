import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_fundamental_table(url, business_date):

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="grid")

    if table is None:
        raise Exception("Table with class='grid' not found")

    rows = table.find_all("tr")

    header1 = rows[0].find_all(["td", "th"])
    header2 = rows[1].find_all(["td", "th"])

    columns = ["Country"]

    groups = []

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

    data = []

    for tr in rows[2:]:

        if "note" in tr.get("class", []):
            continue

        tds = tr.find_all("td")

        if not tds:
            continue

        row = []

        row.append(
            tds[0].get_text(" ", strip=True)
        )

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

    df = pd.DataFrame(data, columns=columns)

    df["BUSINESS_DATE"] = business_date

    return df