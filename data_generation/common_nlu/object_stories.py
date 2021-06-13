from rasa.shared.nlu.state_machine.state_machine_models import (
    Action,
    ActionName,
    BooleanSlot,
    Intent,
    TextSlot,
    Utterance,
)
import data_generation.common_nlu.parameterized_intents as parameterized_intents

import data_generation.common_nlu.common_intents as common
from data_generation.models.story_models import SlotWasSet, Story


import actions.find_objects_action as find_objects_action
import actions.say_object_intros as say_object_intros

from actions import find_objects_action, get_object_info

utter_no_objects_found = Utterance("None objects found")

# Stories for returning attribute given existing context
stories = [
    Story(
        [
            common.intent_when_is_that,
            ActionName("action_set_object_attribute_hours"),
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAMES,
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
                    find_objects_action.SLOT_OBJECT_NAMES,
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
                    find_objects_action.SLOT_OBJECT_NAMES,
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
                    find_objects_action.SLOT_OBJECT_NAMES,
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
                    find_objects_action.SLOT_OBJECT_NAMES,
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
                    find_objects_action.SLOT_OBJECT_NAMES,
                    get_object_info.SLOT_OBJECT_ATTRIBUTE,
                ]
            ),
            ActionName(get_object_info.ACTION_NAME),
        ]
    ),
]

# Find object with type stories
intent_creator = parameterized_intents.intent_is_there_a_type_creator
stories += [
    # Not found case
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
            utter_no_objects_found,
        ]
    ),
    # Found case
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
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAMES,
                ]
            ),
            ActionName(say_object_intros.ACTION_NAME),
        ]
    ),
]

# Find object with activities/places stories
intent_creator = (
    parameterized_intents.intent_is_there_a_place_with_thing_creator
)
stories += [
    # Not found case
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
            utter_no_objects_found,
        ]
    ),
    # Found case
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
            SlotWasSet(
                [
                    find_objects_action.SLOT_OBJECT_NAMES,
                ]
            ),
            ActionName(say_object_intros.ACTION_NAME),
        ]
    ),
]

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


# Get object info stories
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
