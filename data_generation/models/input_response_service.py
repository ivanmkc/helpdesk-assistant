from data_generation.models.story_models import Intent, Story, Utterance

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)

from typing import Optional, List, Tuple
import gspread
import pandas as pd
import os


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
    input_column_names = [
        name
        for name in ["input", "input_canonical", "input_other"]
        if df.get(name) is not None
    ]
    inputs = df[input_column_names].apply(
        lambda x: "\n".join(x.dropna()), axis=1
    )

    responses = ["" for _ in range(df.shape[0])]

    # Apply filters in reverse order so earlier takes precedence
    for filter in reversed(scenario_filter):
        responses = [
            new_response if len(new_response) > 0 else response
            for response, new_response in zip(
                responses, df.get(filter, ["" for _ in range(df.shape[0])])
            )
        ]

    utter_action_ids = df.get(
        "utter_action_id", [None for _ in range(df.shape[0])]
    )

    # Strip all responses
    responses = [response.strip() for response in responses]

    stories = [
        Story(
            [
                IntentWithExamples(examples=input.split("\n")),
                Utterance(response, name=utter_action_id),
            ]
        )
        for input, response, utter_action_id in zip(
            inputs, responses, utter_action_ids
        )
        if len(input) > 0 and len(response) > 0
    ]

    return stories


SERVICE_ACCOUNT_KEY_JSON_PATH = os.getenv("SERVICE_ACCOUNT_KEY_JSON_PATH")


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
    import gspread
    import os

    gc = gspread.service_account(SERVICE_ACCOUNT_KEY_JSON_PATH)
    spreadsheet = gc.open(spreadsheet_name)

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
