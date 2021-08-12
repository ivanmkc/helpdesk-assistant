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


def _pull_stories_from_worksheet(worksheet: gspread.Worksheet) -> List[Story]:
    # Pulls data from the entire spreadsheet tab.
    df = _pull_sheet_data(worksheet)

    # Use data to initialize Document objects
    inputs = list(df["input"].values)
    responses = list(df["response"].values)
    stories = [
        Story(
            [
                IntentWithExamples(examples=input.split("\n")),
                Utterance(response),
            ]
        )
        for input, response in zip(inputs, responses)
    ]

    return stories


def _pull_stories_from_spreadsheet(
    spreadsheet_name: str, worksheet_filter: List[str]
) -> List[Story]:
    gc = gspread.service_account()
    spreadsheet = gc.open(spreadsheet_name)

    all_worksheets = spreadsheet.worksheets()
    if worksheet_filter:
        worksheets = [
            worksheet
            for worksheet in all_worksheets
            if worksheet.title in worksheet_filter
        ]
    else:
        worksheets = all_worksheets

    stories = [
        story
        for worksheet in worksheets
        for story in _pull_stories_from_worksheet(worksheet)
    ]

    return stories


def get_stories(worksheet_filter: List[str]) -> List[Story]:
    SPREADSHEET_NAME = "InputResponseCorpus"
    return _pull_stories_from_spreadsheet(
        spreadsheet_name=SPREADSHEET_NAME, worksheet_filter=worksheet_filter
    )
