from __future__ import print_function
import os.path
import csv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# 1) CHANGE THIS: your Sheet ID (from URL)
SPREADSHEET_ID = ""

# Nazwa zakładki i miejsce wklejenia CSV
SHEET_NAME = ""
RANGE_WRITE = ""

# Ścieżka do pliku CSV, który chcesz wkleić
CSV_PATH = "naklejki.csv"  # <- zmień na swoją nazwę pliku

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("sheets", "v4", credentials=creds)


def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            new_row = []
            for e in row:
                if not "." in e:
                    new_row.append(e)
                    continue
                try:
                    fe = float(e)
                    new_row.append(fe)
                except:
                    new_row.append(e)
            rows.append(new_row)
    return rows


def main():
    service = get_service()

    # 1. Wczytanie danych z CSV
    if not os.path.exists(CSV_PATH):
        print("CSV file not found:", CSV_PATH)
        return

    values = load_csv(CSV_PATH)
    if not values:
        print("CSV is empty, nothing to upload.")
        return

    body = {"values": values}

    print(values)
    # 2. Wklejenie danych do arkusza od A1 w zakładce 'przelewy'
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_WRITE,
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )

    print("Updated cells:", result.get("updatedCells"))


if __name__ == "__main__":
    main()
