"""
This script copies a single report template from one PayAnalytics instance to another.
"""
import sys
import random

from pa_api import pa_get, pa_post

BASE_URL = 'https://some-instance.payanalytics.com/api/v1'
OTHER_BASE_URL = 'https://other-instance.payanalytics.com/api/v1'


def main():
    if len(sys.argv) != 3:
        print_usage_exit()

    auth_token = sys.argv[1]
    other_auth_token = sys.argv[2]

    url_reports = f'{BASE_URL}/report-templates/'
    all_reports = pa_get(url_reports, auth_token)
    report_templates = []
    for report in all_reports:
        if report['data_upload'] is None and report['analysis'] is None:
            # If a report object is neither linked to an upload nor an analysis then
            # it's report template.
            report.pop('id')
            report_templates.append(report)
            for section in report['sections']:
                section.pop('id')

    first_template = report_templates[0]
    first_template['name'] = first_template['name'] + "-" + str(random.randint(0, 999999))

    url_reports_other = f'{OTHER_BASE_URL}/report-templates/'
    pa_post(url_reports_other, other_auth_token, first_template)
    print(report_templates)


def print_usage_exit():
    sys.exit(f"Usage: ./{sys.argv[0]} <auth-token> <other-auth-token>")


if __name__ == "__main__":
    main()
