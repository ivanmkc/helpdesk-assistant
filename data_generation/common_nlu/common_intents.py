from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    IntentWithExamples,
)

from actions import find_objects_action as find_objects_action

intent_affirm = IntentWithExamples(
    name="intent_affirm",
    examples=[
        "yes",
        "yes please",
        "yes I would",
        "please do",
        "yup",
        "yep",
        "that's right",
        "indeed",
        "Yes, please",
        "yeah",
        "sure",
        "yes thanks",
        "That would be great",
        "YES",
        "YUP",
        "Yea",
        "Yeah",
        "Yeah sure",
        "Yep",
        "Yep that's fine",
        "Yep!",
        "Yepp",
        "Yes",
        "Yes I do",
        "Yes please",
        "Yes please!",
        "Yes, I accept",
        "ok",
        "k",
        "okie dokie",
        "Okay",
        "Sure",
        "That's right",
        "Correct",
        "Exactly",
    ],
)

intent_deny = IntentWithExamples(
    name="intent_deny",
    examples=[
        "no",
        "nope",
        "no thanks",
        "not that one",
        "don't use that",
        "please no",
        "no don't do that",
        "no, use abraham.lincoln@example.com",
        "Neither",
        "Never",
        "Nevermind",
        "No thank you",
        "No, not really.",
        "No, thank you",
        "No.",
        "Nopes",
        "Not really",
        "absolutely not",
        "decline",
        "definitely not",
        "deny",
        "na",
        "nah",
        "nah I'm good",
        "Not exactly",
    ],
)


intent_reaction_positive = IntentWithExamples(
    name="intent_reaction_positive",
    examples=[
        "That's great!",
        "Awesome",
        "That's cool",
        "Cool",
        "Great",
        "Good",
    ],
)

intent_reaction_negative = IntentWithExamples(
    name="intent_reaction_negative",
    examples=["That's not good", "Too bad", "I don't like that", "I hate it"],
)

intent_let_me_think = IntentWithExamples(
    examples=[
        "Give me time",
        "Let me think",
    ]
)

intent_changed_my_mind = IntentWithExamples(
    examples=[
        "I changed my mind",
        "Nevermind",
        "Cancel that",
        "Never mind",
        "I don't need it anymore",
        "Nevermind, I don't want it",
        "I don't want it",
        "I'll pass",
        "Actually, I'll skip it",
        "I'm leaving",
    ]
)

intent_what_is_that = IntentWithExamples(
    examples=[
        "What is that?",
        "What's that?",
        "Tell me about that.",
        "Can I hear more about that?",
        "Do you have more details",
    ],
    name="intent_what_is_this",
)

intent_not_sure = IntentWithExamples(
    examples=[
        "I'm not sure",
        "I'm don't know",
        "I can't decide",
        "not sure",
        "dunno",
    ],
    name="intent_not_sure",
)

# intent_duration = IntentWithExamples(
#     examples=[
#         "How long?",
#         "How long is it?",
#         "What's the length?",
#         "How much time does it take?",
#     ],
#     name="intent_how_long",
# )

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
    ],
    name="intent_what_do_you_recommend",
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
