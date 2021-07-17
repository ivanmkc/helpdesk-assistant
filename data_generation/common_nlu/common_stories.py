from rasa.shared.nlu.state_machine.state_machine_models import Utterance

import data_generation.common_nlu.common_intents as common
from data_generation.models.story_models import Or, Story
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    IntentWithExamples,
)


stories_chitchat = [
    Story(
        [
            Or(common.intent_reaction_positive, common.intent_affirm),
            Utterance("Yeah! What else can I help you with?",),
        ]
    ),
    Story(
        [
            common.intent_where_are_you_from,
            Utterance(
                text="I'm from Belfast. It's in northern Ireland",
                name="utter_where_from_response",
            ),
        ]
    ),
    Story(
        [
            common.how_are_you_doing_intent,
            Utterance(
                text="I'm doing great", name="utter_how_are_you_response",
            ),
        ]
    ),
    Story(
        [
            IntentWithExamples(
                examples=[
                    "Are you busy?",
                    "How busy are you?",
                    "Do you have a lot of work?",
                ],
            ),
            Utterance(text="It's not too busy around here as you can see.",),
        ]
    ),
]
