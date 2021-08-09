from rasa.shared.nlu.state_machine.state_machine_models import (
    ActionName,
    Intent,
    Utterance,
)
from data_generation.common_nlu import common_intent_creators
from data_generation.models.story_models import (
    SlotWasSet,
    Story,
    Checkpoint,
    Or,
)


import actions.find_objects_action as find_objects_action
import actions.say_object_intros as say_object_intros

from actions import (
    find_objects_action,
    get_object_info,
    question_answer_action,
)

utter_no_objects_found = ActionName(
    question_answer_action.ACTION_NAME
)  # Utterance("None objects found")

# Stories for returning attribute given existing context
stories = []

# Find object with type stories
find_object_creators = [
    common_intent_creators.intent_is_there_a_type_creator,
    common_intent_creators.intent_is_there_a_place_with_thing_creator,
]

for intent_creator in find_object_creators:
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
                # ActionName(
                #     action_reset_slots_except_found_object_names.ACTION_NAME
                # ),
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
                        find_objects_action.SLOT_FOUND_OBJECT_NAMES,
                    ]
                ),
                ActionName(say_object_intros.ACTION_NAME),  # ActionName(
                #     action_reset_slots_except_found_object_names.ACTION_NAME
                # ),
            ]
        ),
    ]

# Handle what about scenarios
# intent_creator = common_intents.intent_what_about_context_creator
# stories.append(
#     Story(
#         elements=[
#             Intent(
#                 name=intent_creator.name,
#                 entities=[intent_creator.entity_name],
#             ),
#             SlotWasSet(
#                 [
#                     intent_creator.entity_name,
#                 ]
#             ),
#             ActionName(get_object_info.ACTION_NAME),
#             ActionName(
#                 action_reset_slots_except_found_object_names.ACTION_NAME
#             ),
#         ]
#     )
# )


# Get object info stories
for intent_creator in common_intent_creators.intent_creators:
    if intent_creator.object_attribute:
        slot_set_action_name = f"action_set_{get_object_info.SLOT_OBJECT_ATTRIBUTE}_{intent_creator.object_attribute}"

        # Create story
        stories += [
            # Entities found, objects found
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
                    # Set attribute slot
                    # Action should be the one created dynamically above
                    ActionName(slot_set_action_name),
                    SlotWasSet(
                        [
                            # intent_creator.entity_name,
                            get_object_info.SLOT_OBJECT_ATTRIBUTE,
                        ]
                    ),
                    # Find the objects
                    ActionName(find_objects_action.ACTION_NAME),
                    SlotWasSet(
                        [
                            find_objects_action.SLOT_FOUND_OBJECT_NAMES,
                        ]
                    ),
                    ActionName(get_object_info.ACTION_NAME),
                    # Reset all irrelevant slots
                    # ActionName(
                    #     action_reset_slots_except_found_object_names.ACTION_NAME
                    # ),
                ]
            ),
            # Entities, no objects found
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
                    # Set attribute slot
                    # Action should be the one created dynamically above
                    ActionName(slot_set_action_name),
                    SlotWasSet(
                        [
                            # intent_creator.entity_name,
                            get_object_info.SLOT_OBJECT_ATTRIBUTE,
                        ]
                    ),
                    # Find the objects
                    ActionName(find_objects_action.ACTION_NAME),
                    ActionName(get_object_info.ACTION_NAME),
                    # Reset all irrelevant slots
                    # ActionName(
                    #     action_reset_slots_except_found_object_names.ACTION_NAME
                    # ),
                ]
            ),
            # No entities found
            Story(
                elements=[
                    Intent(
                        name=intent_creator.name,
                    ),
                    # SlotWasSet([intent_creator.entity_name,]),
                    # Set attribute slot
                    # Action should be the one created dynamically above
                    ActionName(slot_set_action_name),
                    SlotWasSet(
                        [
                            # intent_creator.entity_name,
                            get_object_info.SLOT_OBJECT_ATTRIBUTE,
                        ]
                    ),
                    # Find the objects
                    # ActionName(find_objects_action.ACTION_NAME),
                    ActionName(get_object_info.ACTION_NAME),
                    # Reset all irrelevant slots
                    # ActionName(
                    #     action_reset_slots_except_found_object_names.ACTION_NAME
                    # ),
                ]
            ),
        ]

# I want to buy
intent_creator = common_intent_creators.intent_i_want_to_buy_creator
stories += [
    # Entities with number, objects found
    Story(
        elements=[
            Or(
                Intent(
                    name=intent_creator.name,
                    entities=[intent_creator.entity_name, "number"],
                ),
                Intent(
                    name=common_intent_creators.intent_context_only_creator.name,
                    entities=[intent_creator.entity_name, "number"],
                ),
            ),
            SlotWasSet([intent_creator.entity_name, "number"]),
            # Find the objects
            ActionName(find_objects_action.ACTION_NAME),
            # Found
            SlotWasSet(
                [
                    find_objects_action.SLOT_FOUND_OBJECT_NAMES,
                ]
            ),
            ActionName("action_buy_object"),
        ]
    ),
    # Entities with number, no objects found
    Story(
        elements=[
            Or(
                Intent(
                    name=intent_creator.name,
                    entities=[intent_creator.entity_name, "number"],
                ),
                Intent(
                    name=common_intent_creators.intent_context_only_creator.name,
                    entities=[intent_creator.entity_name, "number"],
                ),
            ),
            SlotWasSet([intent_creator.entity_name, "number"]),
            # Find the objects
            ActionName(find_objects_action.ACTION_NAME),
            # TODO: Call a common buy action, it checks 'purchasability' and redirects to the appropriate trigger action
            ActionName("action_buy_object"),
        ]
    ),
    # Entities with number only, objects found
    Story(
        elements=[
            Or(
                Intent(
                    name=intent_creator.name,
                    entities=["number"],
                ),
                Intent(
                    name=common_intent_creators.intent_context_only_creator.name,
                    entities=["number"],
                ),
            ),
            SlotWasSet([intent_creator.entity_name, "number"]),
            # Find the objects
            ActionName(find_objects_action.ACTION_NAME),
            # Found
            SlotWasSet(
                [
                    find_objects_action.SLOT_FOUND_OBJECT_NAMES,
                ]
            ),
            ActionName("action_buy_object"),
        ]
    ),
    # Entities with number only, no objects found
    Story(
        elements=[
            Or(
                Intent(
                    name=intent_creator.name,
                    entities=["number"],
                ),
                Intent(
                    name=common_intent_creators.intent_context_only_creator.name,
                    entities=["number"],
                ),
            ),
            SlotWasSet([intent_creator.entity_name, "number"]),
            # Find the objects
            ActionName(find_objects_action.ACTION_NAME),
            # TODO: Call a common buy action, it checks 'purchasability' and redirects to the appropriate trigger action
            ActionName("action_buy_object"),
        ]
    ),
    # Entities, objects found
    Story(
        elements=[
            Or(
                Intent(
                    name=intent_creator.name,
                    entities=[intent_creator.entity_name],
                ),
                Intent(
                    name=common_intent_creators.intent_context_only_creator.name,
                    entities=[intent_creator.entity_name],
                ),
            ),
            SlotWasSet(
                [
                    intent_creator.entity_name,
                ]
            ),
            # Find the objects
            ActionName(find_objects_action.ACTION_NAME),
            # Found
            SlotWasSet(
                [
                    find_objects_action.SLOT_FOUND_OBJECT_NAMES,
                ]
            ),
            ActionName("action_buy_object"),
        ]
    ),
    # Entities, no objects found
    Story(
        elements=[
            Or(
                Intent(
                    name=intent_creator.name,
                    entities=[intent_creator.entity_name],
                ),
                Intent(
                    name=common_intent_creators.intent_context_only_creator.name,
                    entities=[intent_creator.entity_name],
                ),
            ),
            SlotWasSet(
                [
                    intent_creator.entity_name,
                ]
            ),
            # Find the objects
            ActionName(find_objects_action.ACTION_NAME),
            # TODO: Call a common buy action, it checks 'purchasability' and redirects to the appropriate trigger action
            ActionName("action_buy_object"),
        ]
    ),
    # # No entities found
    # Story(
    #     elements=[
    #         Intent(name=intent_creator.name,),
    #         ActionName("action_buy_object"),
    #     ]
    # ),
]

# # Disambiguation
# intent_creator = common_intent_creators.intent_context_only_creator
# stories += [
#     # Entities with number, objects found
#     Story(
#         elements=[
#             Intent(
#                 name=intent_creator.name,
#                 entities=[intent_creator.entity_name, "number"],
#             ),
#             SlotWasSet([intent_creator.entity_name, "number"]),
#             # Find the objects
#             ActionName(disambiguation_action.ACTION_NAME),
#             # Found
#             SlotWasSet([find_objects_action.SLOT_FOUND_OBJECT_NAMES,]),
#             ActionName("action_buy_object"),
#         ]
#     ),
#     # Entities with number, no objects found
#     Story(
#         elements=[
#             Intent(
#                 name=intent_creator.name,
#                 entities=[intent_creator.entity_name, "number"],
#             ),
#             SlotWasSet([intent_creator.entity_name, "number"]),
#             # Find the objects
#             ActionName(disambiguation_action.ACTION_NAME),
#             # TODO: Call a common buy action, it checks 'purchasability' and redirects to the appropriate trigger action
#             ActionName("action_buy_object"),
#         ]
#     ),
#     # Entities, objects found
#     Story(
#         elements=[
#             Intent(
#                 name=intent_creator.name,
#                 entities=[intent_creator.entity_name],
#             ),
#             SlotWasSet([intent_creator.entity_name,]),
#             # Find the objects
#             ActionName(disambiguation_action.ACTION_NAME),
#             # Found
#             SlotWasSet([find_objects_action.SLOT_FOUND_OBJECT_NAMES,]),
#             ActionName("action_buy_object"),
#         ]
#     ),
#     # Entities, no objects found
#     Story(
#         elements=[
#             Intent(
#                 name=intent_creator.name,
#                 entities=[intent_creator.entity_name],
#             ),
#             SlotWasSet([intent_creator.entity_name,]),
#             # Find the objects
#             ActionName(disambiguation_action.ACTION_NAME),
#             # TODO: Call a common buy action, it checks 'purchasability' and redirects to the appropriate trigger action
#             ActionName("action_buy_object"),
#         ]
#     ),
#     # No entities found
#     Story(
#         elements=[
#             Intent(name=intent_creator.name,),
#             ActionName("action_buy_object"),
#         ]
#     ),
# ]

# stories += [
#     Story(
#         elements=[
#             utter_no_objects_found,
#             ActionName(action_reset_slots_except_found_object_names.ACTION_NAME),
#         ]
#     ),
#     Story(
#         elements=[
#             ActionName(get_object_info.ACTION_NAME),
#             ActionName(action_reset_slots_except_found_object_names.ACTION_NAME),
#         ]
#     ),
#     Story(
#         elements=[
#             ActionName(say_object_intros.ACTION_NAME),
#             ActionName(action_reset_slots_except_found_object_names.ACTION_NAME),
#         ]
#     ),
# ]
