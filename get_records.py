"""
This script gets a list of all records from a PayAnalytics instance and writes to an excel file.
"""
import sys
from openpyxl.workbook import Workbook

from pa_api import pa_get

BASE_URL = 'https://some-instance.payanalytics.com/api/v1'


def main():
    if len(sys.argv) != 2:
        print_usage_exit()

    auth_token = sys.argv[1]

    url_uploads = f'{BASE_URL}/data-uploads/'
    uploads = pa_get(url_uploads, auth_token)
    first_upload = uploads['results'][0]

    url_records = f'{url_uploads}{first_upload["id"]}/records/'
    records = pa_get(url_records, auth_token)

    workbook = Workbook()
    sheet = workbook.active
    headers = first_upload['fields']
    sheet.append(headers)
    for row in records:
        sheet.append(row)
    workbook.save('output.xlsx')


def print_usage_exit():
    sys.exit(f"Usage: ./{sys.argv[0]} <auth-token>")


if __name__ == "__main__":
    main()
