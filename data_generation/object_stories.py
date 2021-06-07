from rasa.shared.nlu.state_machine.state_machine_models import (
    Action,
    ActionName,
    BooleanSlot,
    Intent,
    TextSlot,
    Utterance,
)
import data_generation.parameterized_intents as parameterized_intents

import data_generation.common_intents as common
from data_generation.story_generation import (
    Intent,
    SlotWasSet,
    Story,
)
from data_generation.models import Concept, Object


import actions.find_objects_action as find_objects_action

from actions import find_objects_action, get_object_info


# Stories for returning attribute given existing context
stories = [
    Story(
        [
            common.intent_when_is_that,
            SlotWasSet([find_objects_action.SLOT_OBJECT_NAME]),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_what_price,
            SlotWasSet([find_objects_action.SLOT_OBJECT_NAME]),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_what_is_that,
            SlotWasSet([find_objects_action.SLOT_OBJECT_NAME]),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_how_long,
            SlotWasSet([find_objects_action.SLOT_OBJECT_NAME]),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_directions,
            SlotWasSet([find_objects_action.SLOT_OBJECT_NAME]),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
]

# Add place stories
# stories += [
#     Story(
#         [
#             Intent(intent_creator.name),
#             SlotWasSet(
#                 [
#                     OBJECT_NAME_SLOT_NAME,
#                     OBJECT_ATTRIBUTE_SLOT_NAME,
#                 ]
#             ),
#             ActionName(get_object_info.ACTION_NAME),
#         ]
#     )
#     for intent_creator in parameterized_intents.intent_creators
# ]

for intent_creator in parameterized_intents.intent_creators:
    if intent_creator.object_attribute:
        # TODO: Create the action dynamically to set get_object_info.SLOT_OBJECT_ATTRIBUTE to intent_creator.object_attribute

        slot_set_action_name = f"action_set_{get_object_info.SLOT_OBJECT_ATTRIBUTE}_{intent_creator.object_attribute}"

        # Create story
        stories.append(
            Story(
                elements=[
                    Intent(
                        name=intent_creator.name,
                        entities=[find_objects_action.SLOT_OBJECT_NAME],
                    ),
                    ActionName(
                        slot_set_action_name
                    ),  # Action should be the one created dynamically above
                    SlotWasSet(
                        [
                            find_objects_action.SLOT_OBJECT_NAME,
                            get_object_info.SLOT_OBJECT_ATTRIBUTE,
                        ]
                    ),
                    ActionName(get_object_info.ACTION_NAME),
                ]
            )
        )
