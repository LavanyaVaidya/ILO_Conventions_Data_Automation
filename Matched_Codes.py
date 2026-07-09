import requests
from bs4 import BeautifulSoup
from datetime import datetime

business_date = None

HOME_URL = "https://normlex.ilo.org/dyn/nrmlx_en/f?p=NORMLEXPUB:1:0::NO:::"

FUNDAMENTAL_CODES = {
    "C029",
    "P029",
    "C087",
    "C098",
    "C100",
    "C105",
    "C111",
    "C138",
    "C182",
    "C155",
    "C187",
}

response = requests.get(HOME_URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# ----------------------------
# Find "Latest Ratifications"
# ----------------------------

heading = soup.find("h4", string=lambda x: x and x.strip() == "Latest Ratifications")

if heading is None:
    raise Exception("Latest Ratifications section not found.")

# First boxContent = latest month
latest_month = heading.find_next("div", class_="boxContent")

if latest_month is None:
    raise Exception("Latest month section not found.")

# ----------------------------
# Extract convention codes
# ----------------------------

latest_codes = set()

for li in latest_month.select("ol > li"):

    strong = li.find("strong")

    if not strong:
        continue

    code = strong.get_text(strip=True)
    latest_codes.add(code)
    
    # If this is a fundamental convention, capture its date
    if business_date is None and code in FUNDAMENTAL_CODES:

        text = li.get_text(" ", strip=True)

        # Last 11 characters are like "04 Jun 2026"
        date_str = text[-11:]

        business_date = datetime.strptime(
            date_str,
            "%d %b %Y"
        ).strftime("%d-%m-%Y")

print("Latest month codes:", latest_codes)

# ----------------------------
# Check for fundamental conventions
# ----------------------------

matched_codes = latest_codes.intersection(FUNDAMENTAL_CODES)

if matched_codes:
    print("Fundamental convention(s) found:", matched_codes)

    # Call your existing parser here
    # parse_fundamental_table()

else:
    print("No fundamental convention ratified this month.")

# Fundamental convention found
if matched_codes:

    # Find "Ratification comparative data"
    comparative_heading = soup.find(
        lambda tag: tag.name in ["h3", "h4", "h5"]
        and "Ratification comparative data" in tag.get_text()
    )

    if comparative_heading is None:
        raise Exception("Ratification comparative data section not found.")

    # Find "Fundamental Conventions"
    fundamental_text = comparative_heading.find_next(
        string=lambda s: s and "Fundamental Conventions" in s
    )

    if fundamental_text is None:
        raise Exception("Fundamental Conventions section not found.")

    # First link after that text
    fundamental_link = fundamental_text.find_next("a")

    if fundamental_link is None:
        raise Exception("Fundamental Conventions link not found.")

    url = requests.compat.urljoin(
        HOME_URL,
        fundamental_link["href"]
    )

    print(url)
    print(business_date)

    # Now pass this URL into your existing table scraping code