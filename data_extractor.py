from bs4 import BeautifulSoup
from decimal import Decimal
import re
import csv
import sys


def parse_amount(text: str) -> Decimal:
    txt = text.strip().replace('\xa0', ' ')
    txt = txt.replace(' PLN', '').replace(' ', '').replace(',', '.')
    return Decimal(txt)


def extract_account_number(line: str) -> str | None:
    cleaned = line.replace(' ', '')
    m = re.search(r'(\d{10,})', cleaned)
    return m.group(1) if m else None


def parse_html_transactions(path: str):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    header_td = soup.find("td", string=lambda s: s and "Data operacji" in s)
    if header_td is None:
        raise RuntimeError("Nie znaleziono nagłówka 'Data operacji'")

    table = header_td.find_parent("table")
    rows = table.find_all("tr")[1:]  # skip header

    transactions = []
    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 5:
            continue

        date_str = tds[0].get_text(strip=True)

        desc_td = tds[1]
        raw_parts = desc_td.decode_contents().split("<br/>")
        parts = [
            BeautifulSoup(p, "html.parser").get_text(" ", strip=True)
            for p in raw_parts if p.strip()
        ]
        title = parts[0] if parts else ""
        name = title.split(",", 1)[0].strip() if title else ""
        title = title.split(",", 1)[1].strip() if title else ""
        title = title.upper()
        account_number = extract_account_number(parts[-1]) if parts else None

        amount = parse_amount(tds[4].get_text(" ", strip=True))

        transactions.append({
            "date": date_str,
            "title": title,
            "name": name,
            "account_number": account_number,
            "amount": amount,
        })

    return transactions


def print_as_csv(transactions):
    """Print the list of transactions as CSV to stdout."""
    output = open(sys.argv[1][:-4]+"csv", "w", encoding="utf-8")
    
    fieldnames = ["date", "title", "name", "account_number", "amount"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for t in transactions:
        t_out = t.copy()
        # Convert Decimal -> string with comma
        t_out["amount"] = str(t["amount"])#.replace(".", ",")
        writer.writerow(t_out)

def main():
    filename = sys.argv[1]
    transactions = parse_html_transactions(filename)
    print_as_csv(transactions)


if __name__ == "__main__":
    main()
