from homepage import get_fundamental_table_details
from fundamental import scrape_fundamental_table


def main():

    result = get_fundamental_table_details()

    if result is None:
        print("No fundamental convention ratified this month.")
        return

    url, business_date, matched_codes = result

    print("Matched codes:", matched_codes)
    print("Business date:", business_date)

    df = scrape_fundamental_table(
        url,
        business_date
    )

    print(df.head())

    df.to_csv(
        "ILO_Conventions.csv",
        index=False
    )

    print("Saved to ILO_Conventions.csv")


if __name__ == "__main__":
    main()