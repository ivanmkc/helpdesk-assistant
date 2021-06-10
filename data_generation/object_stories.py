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
            ActionName("action_set_object_attribute_hours"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_when_is_that,
            ActionName("action_set_object_attribute_hours"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_what_price,
            ActionName("action_set_object_attribute_price"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_what_is_that,
            ActionName("action_set_object_attribute_details"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_duration,
            ActionName("action_set_object_attribute_duration"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
    Story(
        [
            common.intent_directions,
            ActionName("action_set_object_attribute_directions"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
]

# Find object stories
stories.append(
    Story(
        elements=[
            Intent(
                name=parameterized_intents.intent_is_there_a_context_creator.name,
                entities=[find_objects_action.SLOT_OBJECT_NAME],
            ),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAME,
                ]
            ),
            ActionName(find_objects_action.ACTION_NAME),
        ]
    )
)

# Find object with activities stories
intent_creator = (
    parameterized_intents.intent_is_there_a_place_with_context_creator
)
stories.append(
    Story(
        elements=[
            Intent(
                name=intent_creator.name,
                entities=[intent_creator.entity_name],
            ),
            SlotWasSet(
                [
                    intent_creator.entity_name,
                ]
            ),
            ActionName(find_objects_action.ACTION_NAME),
        ]
    )
)

# Handle what about scenarios
intent_creator = parameterized_intents.intent_what_about_context_creator
stories.append(
    Story(
        elements=[
            Intent(
                name=intent_creator.name,
                entities=[intent_creator.entity_name],
            ),
            SlotWasSet(
                [
                    intent_creator.entity_name,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    )
)


# Get object info stores
for intent_creator in parameterized_intents.intent_creators:
    if intent_creator.object_attribute:
        slot_set_action_name = f"action_set_{get_object_info.SLOT_OBJECT_ATTRIBUTE}_{intent_creator.object_attribute}"

        # Create story
        stories.append(
            Story(
                elements=[
                    Intent(
                        name=intent_creator.name,
                        entities=[intent_creator.entity_name],
                    ),
                    SlotWasSet(
                        [
                            intent_creator.entity_name,
                        ]
                    ),
                    ActionName(
                        slot_set_action_name
                    ),  # Action should be the one created dynamically above
                    SlotWasSet(
                        [
                            intent_creator.entity_name,
                            get_object_info.SLOT_OBJECT_ATTRIBUTE,
                        ]
                    ),
                    ActionName(get_object_info.ACTION_NAME),
                ]
            )
        )
