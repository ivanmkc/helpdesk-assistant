from data_generation.common_nlu.parameterized_intents import (
    ParameterizedIntentCreator,
)

from actions import find_objects_action as find_objects_action

intent_is_there_a_type_creator = ParameterizedIntentCreator(
    name="intent_is_there_a_type_with_entities",
    parameterized_examples=[
        "Is there {context}?",
        "Is there {context} around here?",
        "I want to see {context}",
        "Do you know of any {context}?",
        "Any {context}?",
        "Have you heard about {context}?",
        "You wouldn't know {context}, would you?",
        "Tell me about {context}?",
        "I've heard about {context}",
        "I've heard there was {context}?",
        "I've heard there was {context}. Know anything about that?",
        "Do you know about {context}",
        "Tell me about any {context}",
        "Can you point me towards {context}",
        "What is {context}?",
        "What's {context}?",
        "Tell me about {context}.",
        "Can I hear more about {context}?",
        "Do you have more details about {context}",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)

intent_is_there_a_place_with_thing_creator = ParameterizedIntentCreator(
    name="intent_is_there_a_place_with_context_with_entities",
    parameterized_examples=[
        "Is there a place to {context}?",
        "Is there somewhere to see {context}?",
        "Do you know of any places for {context}?",
        "I want to {context}?",
        "Where can I find {context}?",
        "Where can I get {context}?",
        "Where would I go for {context}?",
        "I'm looking for {context}?",
        "Is there somewhere with {context}",
        "I want to see {context}",
        "Are there {context}?",
        "Are there {context} around here?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)


intent_when_is_that_creator = ParameterizedIntentCreator(
    name="intent_what_hours_with_entities",
    parameterized_examples=[
        "What are the hours of {context}?",
        "What time does {context} happpen?",
        "When does {context} open?",
        "When does {context} close?",
        "What are {context} hours?",
        "When does {context} close?",
        "What time does {context} open until?",
        "What time does {context} close?",
        "Is {context} still open?",
        "When would {context} be open?",
        "When would {context} open?",
        "When would {context} close?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="hours",
)

intent_what_price_creator = ParameterizedIntentCreator(
    name="intent_what_price_with_entities",
    parameterized_examples=[
        "How much is {context}?",
        "Is {context} expensive?",
        "Is {context} cheap?",
        "How much does {context} cost?",
        "What's the cost of {context}?",
        "What's the price of {context}?",
        "How much for {context}?",
        "What price for {context}?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="price",
)

intent_what_duration_creator = ParameterizedIntentCreator(
    name="intent_what_duration_with_entities",
    parameterized_examples=[
        "How long is {context}?",
        "What's the length of {context}?",
        "What's the duration of {context}?",
        "How much time does {context} take?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="duration",
)

intent_directions_creator = ParameterizedIntentCreator(
    name="intent_directions_with_entities",
    parameterized_examples=[
        "How do you get to {context}?",
        "What's the way to {context}?",
        "How do I go to {context}?",
        "What are the directions to {context}?",
        "Do you know where {context} is?",
        "Do you know how to get to {context}?",
        "Where is the closest {context}",
        "Where is {context}",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="directions",
)

intent_ill_have_context_creator = ParameterizedIntentCreator(
    name="intent_i_will_have_with_entities",
    parameterized_examples=[
        "Sure, I'll get {context}",
        "I'll have {context} then",
        "{context} sounds great",
        "Yes, I'll get {context}",
        "I'll have {context}",
        "I'll take {context}",
        "Ya, {context} sounds good",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)

intent_creators = [
    # intent_is_there_a_type_creator,
    # intent_what_is_context_creator,
    # intent_what_about_context_creator,
    intent_directions_creator,
    # intent_is_there_a_place_with_thing_creator,
    intent_when_is_that_creator,
    intent_what_price_creator,
    intent_what_duration_creator,
    # intent_ill_have_context_creator,
]
