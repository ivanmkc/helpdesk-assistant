from rasa.shared.nlu.state_machine.state_machine_models import (
    IntentWithExamples,
)

intent_where_are_you_from = IntentWithExamples(
    name="where_are_you_from", examples=["Where are you from?"]
)

intent_let_me_think = IntentWithExamples(
    examples=[
        "Give me time",
        "Let me think",
    ]
)

intent_what_do_you_do = IntentWithExamples(
    examples=[
        "What do you do here?",
        "How can you help?",
        "What's your job?",
        "What can you do to help me?",
        "Do you have more details",
    ]
)

intent_changed_my_mind = IntentWithExamples(
    examples=[
        "I changed my mind",
        "Nevermind",
        "Cancel that",
        "Never mind",
        "I don't need it anymore",
    ]
)

intent_what_is_that = IntentWithExamples(
    examples=[
        "What is that?",
        "What's that?",
        "Tell me about that.",
        "Can I hear more about that?",
        "Do you have more details",
    ]
)

intent_directions = IntentWithExamples(
    examples=[
        "How do you get there?",
        "What's the way there?",
        "How do I go there?",
        "What are the directions there?",
        "Where is that?",
    ]
)

intent_when_is_that = IntentWithExamples(
    examples=[
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
    ]
)

intent_what_price = IntentWithExamples(
    examples=[
        "How much is it?",
        "Is it expensive?",
        "How much does it cost?",
        "What's the cost?",
        "What's the price?",
        "How much?",
        "What price?",
        "What cost?",
    ]
)

intent_not_sure = IntentWithExamples(
    examples=[
        "I'm not sure",
        "I'm don't know",
        "I can't decide",
        "not sure",
        "dunno",
    ]
)

intent_how_long = IntentWithExamples(
    examples=[
        "How long?",
        "How long is it?",
        "What's the length?",
        "How much time does it take?",
    ]
)

intent_what_do_you_recommend = IntentWithExamples(
    examples=[
        "What do you recommend?",
        "It's up to you",
        "Up to you",
        "Can you help me decide?",
        "Can you give me a recommendation?",
        "Care to give me a recommendation?",
        "Recommend something",
        "Give me a recommendation",
        "What do you think?",
    ]
)

intent_sure_ill_get_that = IntentWithExamples(
    examples=[
        "Sure, I'll get that",
        "I'll have that then",
        "That sounds great",
        "Yes, I'll get that",
        "I'll have that",
        "I'll take one",
        "Ya, that sounds good",
    ]
)

want_to_leave_intent = IntentWithExamples(
    name="want_to_leave",
    examples=[
        "I want to leave",
        "I need to know.",
        "I've got to go.",
        "Sorry, something came up and I have to go.",
        "Can I leave?",
    ],
)


how_are_you_doing_intent = IntentWithExamples(
    name="how_are_you_doing",
    examples=[
        "How are you doing?",
        "How's it going?",
        "How are you?",
        "How is your day going?",
    ],
)
