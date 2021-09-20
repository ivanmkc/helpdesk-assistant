from data_generation.models.chatbot import Chatbot
from data_generation.models.story_models import SlotWasSet, Story
from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    IntentWithExamples,
    Utterance,
)
from rasa.shared.core.slots import TextSlot
from typing import Dict, List
import data_generation.chatbots.input_response.util as util
import string


def convert_to_story(
    question_id: str, question: str, responses: List[str], is_correct: bool
) -> Story:
    text_stripped = "".join(
        e.lower().strip(string.punctuation)
        for e in question
        if e.isalnum() or e.isspace() or e in ["-", "_"]
    )
    text_stripped = "_".join(text_stripped.split(" "))

    return Story(
        [
            IntentWithExamples(
                examples=responses,
                name=text_stripped,
            ),
            Utterance(
                text="Correct" if is_correct else "Incorrect",
                name=f"utter_{question_id}",
            ),
        ]
    )


stories = [
    convert_to_story(
        question_id=response["question_id"],
        question=response["question"],
        responses=response["inputs"],
        is_correct=response["is_correct"],
    )
    for response in util.get_input_responses()
]

# stories = [
#     # set_question_id_story,
#     Story(
#         [
#             IntentWithExamples(
#                 examples=[
#                     "New York",
#                     "I live in New York",
#                     "New York City",
#                     "My house is in New York",
#                 ],
#                 name="new_york_living",
#             ),
#             Utterance(text="Correct! LIVING", name="utter_correct"),
#         ]
#     ),
# ]

chatbot = Chatbot(
    state_machine=None,
    stories=stories,
    objects=[],
    additional_intents=[],
    additional_slots=[
        TextSlot(name="question_id"),
    ],
)
