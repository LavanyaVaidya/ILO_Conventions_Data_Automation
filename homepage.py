import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import HOME_URL, FUNDAMENTAL_CODES


def get_fundamental_table_details():

    business_date = None

    response = requests.get(HOME_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    heading = soup.find(
        "h4",
        string=lambda x: x and x.strip() == "Latest Ratifications"
    )

    if heading is None:
        raise Exception("Latest Ratifications section not found.")

    latest_month = heading.find_next("div", class_="boxContent")

    if latest_month is None:
        raise Exception("Latest month section not found.")

    latest_codes = set()

    for li in latest_month.select("ol > li"):

        strong = li.find("strong")

        if not strong:
            continue

        code = strong.get_text(strip=True)
        latest_codes.add(code)

        if business_date is None and code in FUNDAMENTAL_CODES:

            text = li.get_text(" ", strip=True)

            date_str = text[-11:]

            business_date = datetime.strptime(
                date_str,
                "%d %b %Y"
            ).strftime("%d-%m-%Y")

    matched_codes = latest_codes.intersection(FUNDAMENTAL_CODES)

    if not matched_codes:
        return None

    comparative_heading = soup.find(
        lambda tag: tag.name in ["h3", "h4", "h5"]
        and "Ratification comparative data" in tag.get_text()
    )

    if comparative_heading is None:
        raise Exception("Ratification comparative data section not found.")

    fundamental_text = comparative_heading.find_next(
        string=lambda s: s and "Fundamental Conventions" in s
    )

    if fundamental_text is None:
        raise Exception("Fundamental Conventions section not found.")

    fundamental_link = fundamental_text.find_next("a")

    if fundamental_link is None:
        raise Exception("Fundamental Conventions link not found.")

    url = requests.compat.urljoin(
        HOME_URL,
        fundamental_link["href"]
    )

    return url, business_date, matched_codes