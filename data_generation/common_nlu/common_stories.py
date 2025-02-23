from rasa.shared.nlu.state_machine.state_machine_models import Utterance

import data_generation.common_nlu.common_intents as common
from data_generation.models.story_models import Or, Story


stories_chitchat = [
    Story(
        [
            Or(common.intent_reaction_positive, common.intent_affirm),
            Utterance(
                "Yeah! What else can I help you with?",
            ),
        ]
    ),
]
