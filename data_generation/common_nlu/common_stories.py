from rasa.shared.nlu.state_machine.state_machine_models import Utterance

import data_generation.common_nlu.common_intents as common
from data_generation.models.story_models import Intent, Or, Story


stories_chitchat = [
    Story(
        [
            common.intent_reaction_positive,
            Utterance("Yeah! What else can I help you with?",),
        ]
    ),
]
