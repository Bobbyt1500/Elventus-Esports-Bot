import gspread
import os
import utils.ids as ids

async def update(guild):
    service_account = gspread.service_account(os.getenv("GOOGLE_CREDENTIALS"))
    spreadsheet = service_account.open_by_key(ids.applications_spread_key)
    worksheet = spreadsheet.get_worksheet(0)
    print(worksheet.get_all_values())
    
