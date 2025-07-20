import gspread
from google.oauth2.service_account import Credentials
import os

SERVICE_ACCOUNT_FILE = 'google/service_account.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "RealEstateBotData")


def get_gspread_client():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def get_allowed_objects(telegram_id: str):
    gc = get_gspread_client()
    sheet = gc.open(SPREADSHEET_NAME).worksheet("AccessControl")
    data = sheet.get_all_records()

    return [
        row for row in data
        if str(row["telegram_id"]) == str(telegram_id)
    ]


def get_vendor_credentials(client: str, obj: str):
    gc = get_gspread_client()
    sheet = gc.open(SPREADSHEET_NAME).worksheet("VendorCredentials")
    data = sheet.get_all_records()

    return [
        row for row in data
        if row["client"] == client and row["object"] == obj
    ]
