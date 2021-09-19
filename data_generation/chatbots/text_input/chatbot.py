from data_generation.models.chatbot import Chatbot
from data_generation.models.story_models import SlotWasSet, Story
from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    IntentWithExamples,
    Utterance,
)
from rasa.shared.core.slots import TextSlot

# set_question_id_story = Story(
#     [
#         IntentWithExamples(
#             examples=[
#                 "set slot to [new_york_hometown](question_id)",
#                 "set slot to [new_york_living](question_id)",
#             ],
#             name="set_question_id",
#         ),
#     ]
# )

stories = [
    # set_question_id_story,
    Story(
        [
            IntentWithExamples(
                examples=[
                    "New York",
                    "I live in New York",
                    "New York City",
                    "My house is in New York",
                ],
                name="new_york_living",
            ),
            Utterance(text="Correct! LIVING", name="utter_correct"),
        ]
    ),
]

chatbot = Chatbot(
    state_machine=None,
    stories=stories,
    objects=[],
    additional_intents=[],
    additional_slots=[
        TextSlot(name="question_id"),
    ],
)
