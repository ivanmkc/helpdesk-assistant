from data_generation.models.story_models import Intent, Story, Utterance

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)

from typing import Optional, List, Tuple
import gspread
import pandas as pd


def _pull_sheet_data(worksheet) -> pd.DataFrame:
    data = worksheet.get_all_values()
    headers = data.pop(0)

    return pd.DataFrame(data, columns=headers)


def _pull_stories_from_worksheet(
    worksheet: gspread.Worksheet, scenario_filter: List[str]
) -> List[Story]:
    # Pulls data from the entire spreadsheet tab.
    df = _pull_sheet_data(worksheet)

    # Use data to initialize Document objects
    inputs = list(df["input"].values)
    responses = ["" for _ in range(df.shape[0])]

    # Apply filters in reverse order so earlier takes precedence
    for filter in reversed(scenario_filter):
        responses = [
            new_response if len(new_response) > 0 else response
            for response, new_response in zip(
                responses, df.get(filter, ["" for _ in range(df.shape[0])])
            )
        ]

    # Strip all responses
    responses = [response.strip() for response in responses]

    stories = [
        Story(
            [
                IntentWithExamples(examples=input.split("\n")),
                Utterance(response),
            ]
        )
        for input, response in zip(inputs, responses)
        if len(input) > 0 and len(response) > 0
    ]

    return stories


KEY_JSON_PATH = "./key.json"


def extract_bucket_and_prefix_from_gcs_path(
    gcs_path: str,
) -> Tuple[str, Optional[str]]:
    """Given a complete GCS path, return the bucket name and prefix as a tuple.
    Example Usage:
        bucket, prefix = extract_bucket_and_prefix_from_gcs_path(
            "gs://example-bucket/path/to/folder"
        )
        # bucket = "example-bucket"
        # prefix = "path/to/folder"
    Args:
        gcs_path (str):
            Required. A full path to a Google Cloud Storage folder or resource.
            Can optionally include "gs://" prefix or end in a trailing slash "/".
    Returns:
        Tuple[str, Optional[str]]
            A (bucket, prefix) pair from provided GCS path. If a prefix is not
            present, a None will be returned in its place.
    """
    if gcs_path.startswith("gs://"):
        gcs_path = gcs_path[5:]
    if gcs_path.endswith("/"):
        gcs_path = gcs_path[:-1]

    gcs_parts = gcs_path.split("/", 1)
    gcs_bucket = gcs_parts[0]
    gcs_blob_prefix = None if len(gcs_parts) == 1 else gcs_parts[1]

    return (gcs_bucket, gcs_blob_prefix)


def _pull_stories_from_spreadsheet(
    spreadsheet_name: str, scenario_filter: List[str]
) -> List[Story]:
    import google.auth
    import gspread
    import google.cloud.storage as storage
    import os

    # try:
    #     credentials, project_id = google.auth.default(
    #         scopes=[
    #             "https://spreadsheets.google.com/feeds",
    #             "https://www.googleapis.com/auth/drive",
    #             "https://www.googleapis.com/auth/spreadsheets",
    #         ]
    #     )
    #     gc = gspread.authorize(credentials)
    #     spreadsheet = gc.open(spreadsheet_name)
    # except Exception as exception:
    # (
    #     key_file_bucket_name,
    #     key_file_blob,
    # ) = extract_bucket_and_prefix_from_gcs_path(
    #     os.getenv("SERVICE_ACCOUNT_KEY_FILE_URI")
    # )

    # # Download auth file
    # storage_client = storage.Client()
    # # Create a bucket object for our bucket
    # bucket = storage_client.get_bucket(key_file_bucket_name)
    # # Create a blob object from the filepath
    # blob = bucket.blob(key_file_blob)
    # # Download the file to a destination
    # blob.download_to_filename(KEY_JSON_PATH)

    gc = gspread.service_account(KEY_JSON_PATH)
    spreadsheet = gc.open(spreadsheet_name)

    # Remove file when finished
    os.remove(KEY_JSON_PATH)

    stories = [
        story
        for worksheet in spreadsheet.worksheets()
        for story in _pull_stories_from_worksheet(worksheet, scenario_filter)
    ]

    return stories


def get_stories(scenario_filter: List[str]) -> List[Story]:
    """
    Apply scenario filters to responses from multiple columns. Order of precedence matches the order of filteres.
    """

    SPREADSHEET_NAME = "InputResponseCorpus"
    return _pull_stories_from_spreadsheet(
        spreadsheet_name=SPREADSHEET_NAME, scenario_filter=scenario_filter
    )
