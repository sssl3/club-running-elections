import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def read_private_sheet(url, keyfile):
    scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
    ]   
    creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url(url)
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df = df.drop(df.columns[0], axis=1)
    return df

def read_public_sheet(url):
    df = pd.read_csv(url)
    df = df.drop(df.columns[0], axis=1)
    return df