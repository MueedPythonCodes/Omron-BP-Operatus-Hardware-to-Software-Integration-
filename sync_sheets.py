import gspread
from google.oauth2.service_account import Credentials
import json
import os
from config import Config

class GoogleSheetsHandler:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.initialized = False

    def initialize(self):
        print("   🔄 Attempting Google Sheets connection...")
        try:
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_file(Config.GOOGLE_CREDENTIALS_FILE, scopes=scope)
            self.client = gspread.authorize(creds)
            print("   ✅ Authorized with service account")

            spreadsheet = self.client.open_by_key(Config.GOOGLE_SHEET_ID)
            print(f"   ✅ Opened spreadsheet")

            try:
                self.sheet = spreadsheet.worksheet(Config.WORKSHEET_NAME)
                print(f"   ✅ Found worksheet: {Config.WORKSHEET_NAME}")
            except gspread.exceptions.WorksheetNotFound:
                print(f"   ⚠️ Worksheet not found, creating...")
                self.sheet = spreadsheet.add_worksheet(title=Config.WORKSHEET_NAME, rows=100, cols=10)
                headers = ["BPM", "Date", "Datetime Full", "DIA", "SYS", "Time", "User"]
                self.sheet.update('A1:G1', [headers])
                print("   ✅ New worksheet created with headers")

            self.initialized = True
            print("   ✅ Google Sheets fully initialized!")
            return True
        except Exception as e:
            print(f"   ❌ FATAL: Connection failed - {e}")
            self.initialized = False
            return False

    def upload_to_sheets(self):
        print("   🚀 Starting upload to Google Sheets...")
        if not self.initialized:
            print("   ⚠️ Not initialized, trying now...")
            if not self.initialize():
                print("   ❌ Initialization failed, aborting upload")
                return

        try:
            if not os.path.exists(Config.DATA_FILE):
                print(f"   ⚠️ {Config.DATA_FILE} not found!")
                return

            with open(Config.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"   ✅ Loaded data from ubpm.json: SYS={data.get('sys')}, DIA={data.get('dia')}, BPM={data.get('bpm')}")

            row_data = [
                data.get('bpm', '--'),
                data.get('date', '--'),
                data.get('datetime_full', '--'),
                data.get('dia', '--'),    # DIA column
                data.get('sys', '--'),    # SYS column
                data.get('time', '--'),
                data.get('user', '--')
            ]

            self.sheet.update('A2:G2', [row_data])
            print("   🎉 SUCCESS: Latest reading uploaded to Google Sheets Row 2!")

        except Exception as e:
            print(f"   ❌ Upload failed: {e}")

handler = GoogleSheetsHandler()

def upload_to_sheets():
    handler.upload_to_sheets()