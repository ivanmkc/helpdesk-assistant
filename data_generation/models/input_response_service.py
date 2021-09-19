from data_generation.models.story_models import Intent, Story, Utterance

from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)

from typing import List
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
            for response, new_response in zip(responses, df.get(filter, []))
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


def _pull_stories_from_spreadsheet(
    spreadsheet_name: str, scenario_filter: List[str]
) -> List[Story]:
    gc = gspread.service_account()
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
