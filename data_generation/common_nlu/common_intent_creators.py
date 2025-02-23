from data_generation.common_nlu.parameterized_intents import (
    ParameterizedIntentCreator,
)

from actions import find_objects_action as find_objects_action

intent_is_there_a_type_creator = ParameterizedIntentCreator(
    name="intent_is_there_a_type_with_entities",
    parameterized_examples=[
        "Is there <context>?",
        "Is there <context> around here?",
        "I want to see <context>",
        "Do you know of any <context>?",
        "Any <context>?",
        "Have you heard about <context>?",
        "You wouldn't know <context>, would you?",
        "I've heard about <context>",
        "I've heard there was <context>?",
        "I've heard there was <context>. Know anything about that?",
        "Do you know about <context>",
        "Tell me about any <context>",
        "Can you point me towards <context>",
        "What is <context>?",
        "What's <context>?",
        "Tell me about <context>.",
        "I want to learn more about <context>",
        "What about other <context>",
        "What about <context>",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)

intent_is_there_a_place_with_thing_creator = ParameterizedIntentCreator(
    name="intent_is_there_a_place_with_context_with_entities",
    parameterized_examples=[
        "Is there a place to <context>?",
        "Is there somewhere to see <context>?",
        "Do you know of any places for <context>?",
        "I want to <context>?",
        "Where can I find <context>?",
        "Where can I get <context>?",
        "Where would I go for <context>?",
        "I'm looking for <context>?",
        "Is there somewhere with <context>",
        "I want to see <context>",
        "Are there <context>?",
        "Are there <context> around here?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)


intent_when_is_that_creator = ParameterizedIntentCreator(
    name="intent_what_hours_with_entities",
    parameterized_examples=[
        "What are the hours of <context>?",
        "What time does <context> happpen?",
        "When does <context> open?",
        "When does <context> close?",
        "What are <context> hours?",
        "When does <context> close?",
        "What time does <context> open until?",
        "What time does <context> close?",
        "Is <context> still open?",
        "When would <context> be open?",
        "When would <context> open?",
        "When would <context> close?",
        "When is that?",
        "What are the hours?",
        "What time does that happpen?",
        "When does it open?",
        "When does it close?",
        "What are the hours?",
        "When does it close?",
        "What time does it open?",
        "What time does it open until?",
        "What time does it close?",
        "Is it still open?",
        "What would be the hours?",
        "What would the hours be?",
        "Do you know when it opens?",
        "When are they open?",
        "When do they close?",
        "When would they be closing?",
        "What time does are they open?",
        "Are they open now?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="hours",
)

intent_what_price_creator = ParameterizedIntentCreator(
    name="intent_what_price_with_entities",
    parameterized_examples=[
        "How much is <context>?",
        "Is <context> expensive?",
        "Is <context> cheap?",
        "How much does <context> cost?",
        "What's the cost of <context>?",
        "What's the price of <context>?",
        "How much for <context>?",
        "What price for <context>?",
        "How much is it?",
        "Is it expensive?",
        "How much does it cost?",
        "What's the cost?",
        "What's the price?",
        "How much?",
        "What price?",
        "What cost?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="price",
)

intent_what_duration_creator = ParameterizedIntentCreator(
    name="intent_what_duration_with_entities",
    parameterized_examples=[
        "How long is <context>?",
        "What's the length of <context>?",
        "What's the duration of <context>?",
        "How much time does <context> take?",
        "How long?",
        "How long is it?",
        "What's the length?",
        "How much time does it take?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="duration",
)

intent_directions_creator = ParameterizedIntentCreator(
    name="intent_directions_with_entities",
    parameterized_examples=[
        "How do you get to <context>?",
        "What's the way to <context>?",
        "How do I go to <context>?",
        "What are the directions to <context>?",
        "Do you know where <context> is?",
        "Do you know how to get to <context>?",
        "Where is the closest <context>",
        "Where is <context>",
        "Cool! Where is it?",
        "Where is it?",
        "What is that?",
        "How do you get there?",
        "Can you give directions?",
        "How does one get there?",
        "Any idea how to get there?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="directions",
)

intent_opinion_creator = ParameterizedIntentCreator(
    name="intent_opinion_with_entities",
    parameterized_examples=[
        "What do you think of <context>?",
        "What your opinion of <context>?",
        "Do you like <context>?",
        "What's your opinion of <context>?",
        "Don't you like <context>?",
        "What do you think about <context>?",
        "What are your thoughts on <context>?",
        "Can I hear more about <context>?",
        "Do you have more details about <context>",
        "What do you think about it?",
        "Do you like it?",
        "What's your opinion of it?",
        "What's your opinion?",
        "What do you think?",
        "What are your thoughts?",
        "Thoughts?",
        "You like?",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="opinion",
)

intent_details_creator = ParameterizedIntentCreator(
    name="intent_details",
    parameterized_examples=[
        "What's there to do at <context>?",
        "What's in <context>",
        "What things do you do at <context>?",
        "Tell me more about the <context>",
        "What's there to know about <context>",
        "What's there to do?",
        "What do you do here?",
        "What can you do there",
        "Is there anything to do?",
        "What's there to do?",
        "What activities are there?",
        "What kind of things do you do at <context>",
        "What's there to do around here",
        "Tell me more about this place",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
    object_attribute="details",
)

# intent_ill_have_context_creator = ParameterizedIntentCreator(
#     name="intent_i_will_have_with_entities",
#     parameterized_examples=[
#         "Sure, I'll get <context>",
#         "I'll have <context> then",
#         "<context> sounds great",
#         "Yes, I'll get <context>",
#         "I'll have <context>",
#         "I'll take <context>",
#         "Ya, <context> sounds good",
#     ],
#     entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
# )

buy_synonyms = "[buy|order|get|have|need|want|book|take]"

intent_i_want_to_buy_creator = ParameterizedIntentCreator(
    name="intent_i_want_to_buy_with_entities",
    parameterized_examples=[
        f"I want to {buy_synonyms} <number> <context>",
        f"Can I {buy_synonyms} <number> <context>?",
        f"I'll {buy_synonyms} <number> <context>?",
        "Give me <number> <context>?",
        f"I {buy_synonyms} <number> <context>?",
        f"We {buy_synonyms} get <number> <context>",
        "Let me [have|get] <number> <context>",
        f"I {buy_synonyms} <number> <context>",
        f"Sure, I'll {buy_synonyms} <number> <context>",
        f"I'll {buy_synonyms} <number> <context> then",
        "<number> <context> sounds great",
        f"Yes, I'll {buy_synonyms} <number> <context>",
        f"I'll {buy_synonyms} <number> <context>",
        f"I'll {buy_synonyms} <number> <context>",
        "Ya, <context> sounds good",
        f"I'll {buy_synonyms} <number_only>",
        f"I'll {buy_synonyms} it",
        f"Can I {buy_synonyms} <number_only>?",
        "Give us <number> please",
        f"I'll {buy_synonyms} <number> <context>",
        f"I want to {buy_synonyms} <number> <context>",
        f"Can I {buy_synonyms} <context>",
        f"Can I {buy_synonyms} for <number> people",
        f"I {buy_synonyms} <number_only>",
        f"Ok... I {buy_synonyms} to do the <context>",
        f"Sure thing... I {buy_synonyms} the <context>",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)

intent_context_only_creator = ParameterizedIntentCreator(
    name="intent_context_only",
    parameterized_examples=[
        "<number> <context>",
    ],
    entity_name=find_objects_action.SLOT_OBJECT_NAME_OR_TYPE,
)

intent_creators = [
    # intent_is_there_a_type_creator,
    # intent_what_is_context_creator,
    # intent_what_about_context_creator,
    intent_directions_creator,
    intent_opinion_creator,
    intent_details_creator,
    # intent_is_there_a_place_with_thing_creator,
    intent_when_is_that_creator,
    intent_what_price_creator,
    intent_what_duration_creator,
    # intent_ill_have_context_creator,
]
