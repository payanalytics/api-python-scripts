"""
This script uploads a dataset to PayAnalytics and runs an analysis on it.
"""
import sys
import random
import time
from pprint import pprint

from pa_api import pa_get, pa_post

BASE_URL = 'https://some-instance.payanalytics.com/api/v1'

GENDER_MALE = "m"
GENDER_FEMALE = "f"
GENDER_NONBINARY = "nb"

EMPLOYEE_ID_FIELDNAME = "employee_id"
MAIN_EMPLOYEE_CHARACTERIZATION_FIELD = "division"
GENDER_FIELDNAME = "gender"
SALARY_FIELDNAME = "salary"
GENDER_MAPPING = {
    "male": str(GENDER_MALE),
    "female": str(GENDER_FEMALE),
    "notReported": None,
    "nonBinary": str(GENDER_NONBINARY),
}

FIELDS = [
    EMPLOYEE_ID_FIELDNAME,
    GENDER_FIELDNAME,
    MAIN_EMPLOYEE_CHARACTERIZATION_FIELD,
    "experience_months",
    SALARY_FIELDNAME,
]

RECORDS = [
    [1, GENDER_FEMALE, "marketing", 12, 120000],
    [2, GENDER_MALE, "engineering", 33, 160000],
    [3, GENDER_FEMALE, "engineering", 25, 200000],
    [4, GENDER_FEMALE, "engineering", 25, 240000],
    [5, GENDER_MALE, "engineering", 22, 240000],
    [6, GENDER_MALE, "marketing", 8, 110000],
    [7, GENDER_FEMALE, "engineering", 25, 250000],
    [8, GENDER_FEMALE, "marketing", 25, 160000],
    [9, GENDER_NONBINARY, "marketing", 8, 320000],
    [10, GENDER_FEMALE, "engineering", 25, 180000],
    [11, GENDER_FEMALE, "marketing", 12, 110000],
    [12, GENDER_MALE, "engineering", 33, 190000],
    [13, GENDER_FEMALE, "engineering", 25, 230000],
    [14, GENDER_FEMALE, "engineering", 25, 140000],
    [15, GENDER_MALE, "engineering", 22, 280000],
    [16, GENDER_MALE, "marketing", 8, 100000],
    [17, GENDER_FEMALE, "engineering", 25, 180000],
    [18, GENDER_FEMALE, "marketing", 25, 190000],
    [19, GENDER_NONBINARY, "marketing", 8, 360000],
    [20, GENDER_FEMALE, "engineering", 25, 220000],
    [21, GENDER_MALE, "marketing", 25, 160000],
]


def main():
    if len(sys.argv) != 2:
        print_usage_exit()

    auth_token = sys.argv[1]

    # Step 1: Upload dataset.

    url_uploads = f'{BASE_URL}/data-uploads/'
    upload = {
        "identifier": "demo-%d" % (random.randint(0, 100000),),
        "fields": FIELDS,
        "employee_id_field": EMPLOYEE_ID_FIELDNAME,
        "main_employee_characterization_field": MAIN_EMPLOYEE_CHARACTERIZATION_FIELD,
        "gender_field": GENDER_FIELDNAME,
        "salary_field": SALARY_FIELDNAME,
        "records": RECORDS,
        "gender_mapping": GENDER_MAPPING,
        "default_first_demographic_variable": GENDER_FIELDNAME,
        "default_second_demographic_variable": None,
    }
    data_upload = pa_post(url_uploads, auth_token, upload)

    # Step 2: Find the preset to use.

    url_presets = f"{BASE_URL}/job-configs/"
    all_presets = pa_get(url_presets, auth_token)
    my_preset = None
    for p in all_presets:
        if p['identifier'] == 'my-demo-preset':
            my_preset = p
    if my_preset is None:
        raise ValueError(f"Could not find preset {my_preset}")

    # Step 3: Run an analysis on the dataset using the preset.

    analysis_post_config = {
        "job_config": my_preset["id"],
    }

    url_run_analysis = f"{BASE_URL}/data-uploads/{data_upload['id']}/run-analysis/"
    job_token_info = pa_post(
        url_run_analysis,
        auth_token,
        analysis_post_config
    )
    if job_token_info["returncode"] != 0:
        raise ValueError(
            "Error configuring job, error code: %d" % (job_token_info["returncode"],)
        )

    # Step 4: Ask the service every 500ms whether the job is done.

    job_token_id = job_token_info["content"]["job_token_id"]
    analysis_id = -1
    print("Waiting for analysis job...")
    while analysis_id < 0:
        token_status = pa_get(f"{BASE_URL}/job-tokens/{job_token_id}/", auth_token)
        if token_status["is_done"]:
            if not token_status["is_successful"]:
                raise ValueError(token_status["message"])
            else:
                analysis_id = token_status["response"]["job_result_id"]
        else:
            print("Still running analysis...")
            time.sleep(0.5)

    # Step 5: Get and print the analysis result

    url_analysis = f"{BASE_URL}/analysis-results-simple/{analysis_id}/"
    analysis = pa_get(url_analysis, auth_token)

    pprint(analysis, indent=2)


def print_usage_exit():
    sys.exit(f"Usage: ./{sys.argv[0]} <auth-token>")


if __name__ == "__main__":
    main()
