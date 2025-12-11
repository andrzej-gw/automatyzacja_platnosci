import sys

import data_extractor
import update_sheet

data_extractor.main()
update_sheet.SPREADSHEET_ID = "1D595F88QhG5aa4APNLVfC5SDGB2CZcuNDGe08HdH9Mk"
update_sheet.SHEET_NAME = "przelewy"
update_sheet.RANGE_WRITE = f"{update_sheet.SHEET_NAME}!A1"
update_sheet.CSV_PATH = sys.argv[1][:-4]+"csv"
update_sheet.main()
