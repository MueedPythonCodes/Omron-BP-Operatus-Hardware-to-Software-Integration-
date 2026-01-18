import os

class Config:
    # 1. New Sheet ID (Aapke browser URL se li gayi hai)
    GOOGLE_SHEET_ID = '1gyKVcTcjLxF8DQqTT6u34f66OsxeTzuEr1K5eAKOG80'
    
    # 2. Exact Tab Name (Jo niche neelay rang mein hai)
    WORKSHEET_NAME = 'BP_Readings'
    
    # Baaki settings wahi rahengi
    GOOGLE_CREDENTIALS_FILE = 'service_account.json'
    DATA_FILE = 'ubpm.json'
    DEVICE_NAME = 'hem-7361t'
    MAC_ADDRESS = '00:5F:BF:2B:63:A8'







