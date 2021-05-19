from typing import Any, Dict, List, Set
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    TextSlot,
    BooleanSlot,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Response,
    StateMachineState,
    Transition,
)

from rasa.shared.nlu.state_machine.conditions import (
    IntentCondition,
    OnEntryCondition,
    SlotEqualsCondition,
)

from data_generation import state_machine_generation, story_generation
from data_generation.story_generation import ActionName, IntentName

wheres_the_washroom_intent = Intent(
    name="wheres_the_washroom",
    examples=[
        "Where's the washroom?",
        "Where is the restroom?",
        "What is the location of the washroom?",
        "I need to find the toilet",
    ],
)

select_salad = Intent(
    name="select_salad",
    examples=[
        "I'll have the salad",
        "I want the salad",
        "The salad",
        "The greens",
    ],
)

select_soup = Intent(
    name="select_soup",
    examples=[
        "I'll have the cauliflower",
        "The soup",
        "The cauliflower soup please",
    ],
)

select_tatare = Intent(
    name="select_tatare",
    examples=[
        "I'll have the tuna tatare",
        "Tatare",
        "Tuna",
        "The tuna tatare",
    ],
)

select_generic = Intent(
    name="select_generic",
    examples=[
        "I'll have the [steak](entree)",
        "I'll have the [fish](entree)",
        "I'll try the [fish](entree)",
        "Can I get the [fish](entree)",
        "Why don't I try the [steak](entree)",
        "Get me the [fish](entree)",
        "Get me the [lasagna](entree)",
        "I'll take a [salad](appetizer)",
        "I'll go with the [tatare](appetizer)",
    ],
)

select_fish = Intent(
    name="select_fish",
    examples=[
        "I'll have the fish please",
        "I'd like the sea bass",
        "Sea bass",
        "Can I get the fish?",
        "The fish",
    ],
)

select_steak = Intent(
    name="select_steak",
    examples=[
        "I'll have the beef",
        "Can I get the steak?",
        "Steak please",
        "I'll take the beef",
        "Can I get the steak?",
        "I'll just have the steak",
        "Steak is what I want",
        "Steak",
    ],
)

select_vegetables = Intent(
    name="select_vegetables",
    examples=[
        "I'll have the vegetarian lasagna",
        "The lasagna please",
        "I'll have the vegetarian option",
        "The lasagna for me." "Lasagna",
        "I'll get the lasagna",
    ],
)

# What is lasagna?
# What is the special?
# How much is it?
# Do you have vegetarian food?
# Do you have a kids menu?
# Ask about specials
# Ask for recommendations
# What's an entree

action_ask_appetizer = Utterance(
    "What would you like for your appetizer?", name="utter_ask_appetizer"
)

action_ask_entree = Utterance(
    "What would you like for your entree?", name="utter_ask_entree"
)

slot_appetizer = TextSlot(
    name="appetizer",
    intents={
        select_salad: "salad",
        select_soup: "soup",
        select_tatare: "tatare",
    },
    prompt_actions=[
        action_ask_appetizer,
    ],
)

slot_entree = TextSlot(
    name="entree",
    intents={
        select_fish: "fish",
        select_steak: "steak",
        select_vegetables: "lasagna",
    },
    prompt_actions=[action_ask_entree],
)

steak_doneness_rare = Intent(
    examples=["Rare", "I'd like it raw", "Not cooked"]
)

steak_doneness_mediumrare = Intent(
    examples=["Medium-rare", "Not too cooked", "I want it medium-rare"]
)

steak_doneness_medium = Intent(examples=["Medium"])

steak_doneness_welldone = Intent(examples=["Well-done", "I want it well-done"])

slot_steak_doneness = TextSlot(
    name="steak_doneness",
    condition=SlotEqualsCondition(slot=slot_entree, value="steak"),
    intents={
        steak_doneness_rare: "rare",
        steak_doneness_mediumrare: "medium-rare",
        steak_doneness_medium: "medium",
        steak_doneness_welldone: "well-done",
    },
    prompt_actions=[
        Utterance("How would you like your steak?"),
    ],
)

slot_order_confirmed = BooleanSlot(
    name="order_confirmed",
    intents={
        "affirm": True,
        "deny": False,
    },
    prompt_actions=[
        Utterance(
            "Okay, just to confirm. For your appetizer, you'll have the {appetizer} and for your entree, you'll have the {entree}. Is that correct?"
        ),
    ],
    only_fill_when_prompted=True,
)


generalResponses: List[Response] = [
    Response(
        condition=IntentCondition(common.intent_where_are_you_from),
        actions=[
            Utterance(text="I'm from Canada", name="utter_where_from_response")
        ],
    ),
    Response(
        condition=IntentCondition(how_are_you_doing_intent),
        actions=[
            Utterance(
                text="I'm doing great",
                name="utter_how_are_you_response",
            )
        ],
    ),
    Response(
        condition=IntentCondition(
            Intent(
                name="what_are_hours",
                examples=[
                    "What are your hours?",
                    "When do you close?",
                    "What time do you open until?",
                    "What time do you close?",
                    "Are you still open?",
                ],
            )
        ),
        actions=[
            Utterance(
                text="We're open from 11am to 9pm, every day except Sunday.",
                name="utter_hours",
            )
        ],
    ),
    Response(
        condition=IntentCondition(
            Intent(
                examples=[
                    "Are you busy?",
                    "How busy are you?",
                    "Do you have a lot of work?",
                ],
            )
        ),
        actions=[
            Utterance(
                text="It's not too busy around here as you can see.",
            )
        ],
    ),
]

# TODO: Add a drink

# student_life_state_machine = StateMachineState(
#     name="restaurant_ordering",
#     slots=[
#         SlotGroup([slot_appetizer, slot_entree])
#             .if(SlotEqualsCondition(slot_entree, "steak"), then=SlotGroup(slot_steak_doneness, slot_order_confirmed))
#             .then(slot_order_confirmed)
#     ]
# )

student_life_state_machine = StateMachineState(
    name="restaurant_ordering",
    slots=[
        slot_appetizer,
        slot_entree,
        slot_steak_doneness,
        slot_order_confirmed,
    ],
    slot_fill_utterances=[
        Utterance("The {appetizer} is a great starter."),
        Utterance("Nice, they make a mean {entree} here."),
        Utterance(
            text="Great choices. The {appetizer} goes great with the {entree}"
        ),
    ],
    transitions=[
        Transition(
            name="leave",
            condition=IntentCondition(want_to_leave_intent),
            transition_utterances=[
                Utterance(
                    text="I guess you can leave if you need to, since we haven't made the food yet.",
                    name="utter_leave_response",
                )
            ],
            destination_state_name=None,
        )
    ],
    responses=[
        Response(
            condition=OnEntryCondition(),
            actions=[
                Utterance("Welcome to Michi Cafe"),
                Utterance(
                    "Take your time looking through the menu. I'll be back in 5 minutes for your order."
                ),
                Utterance("Okay, let's take your order."),
            ],
        ),
        Response(
            condition=IntentCondition(
                Intent(
                    examples=[
                        "Can I see a menu?",
                        "Menu please.",
                        "What's on the menu?",
                        "What do you have today?",
                        "What is on your menu?",
                        "What do you have?",
                        "What you have?",
                        "What food is there?",
                        "What are the specials?",
                    ]
                )
            ),
            actions=[
                Utterance(
                    "For our appetizers, we have a Greek salad, a celery soup and a salmon tatare."
                ),
                Utterance(
                    "For entrees, we have a tenderloin steak, a grilled sea bass and a vegetarian lasagna."
                ),
            ],
        ),
        Response(
            condition=IntentCondition(
                Intent(
                    examples=[
                        "What's in the lasagna?",
                        "What's kind of lasagna is it?",
                        "What type of lasagna is it?",
                    ]
                )
            ),
            actions=[
                Utterance(
                    "The lasagna has carrots, zucchini and onion. It also has cottage cheese though, in case you were wondering."
                ),
            ],
        ),  # Followup: So it's not vegan then? Bot: No, it's not vegan
        Response(
            condition=SlotEqualsCondition(
                slot=slot_order_confirmed, value=False
            ),
            actions=[
                Utterance("No? Okay, we can try again."),
                # ResetSlotsAction(
                #     [slot_appetizer, slot_entree, slot_order_confirmed]
                # ),
            ],
        ),
        Response(
            condition=SlotEqualsCondition(
                slot=slot_order_confirmed, value=True
            ),
            actions=[
                Utterance(
                    "Okay great, please enjoy yourself while the food is being readied."
                ),
                # SetSlotsAction(
                #     [slot_appetizer, slot_entree, slot_order_confirmed]
                # ),
            ],
        ),
    ]
    + generalResponses,
)

state_machine_generation.persist(
    student_life_state_machine,
    states_filename="state_machines/restaurant/ordering.yaml",
    domain_filename="domain/restaurant/ordering.yaml",
    nlu_filename="data/restaurant/ordering.yaml",
)

from data_generation.story_generation import Story, Fork, Or

# Descriptions of the food

# Recommendations
story_generation.persist(
    [
        Story(
            name="recommend_appetizer",
            elements=[
                action_ask_appetizer,
                Or(
                    intent_what_do_you_recommend,
                    intent_not_sure,
                    IntentName("help"),
                ),
                Utterance(
                    "May I recommend the tatare? It's our most popular starter."
                ),
                Fork(
                    [
                        Or(intent_sure_ill_get_that, IntentName("affirm")),
                        Utterance("Great, the tatare it is then."),
                        # TODO: Set slot
                        ActionName("action_set_appetizer_tatare"),
                    ],
                    [
                        IntentName("deny"),
                        Utterance(
                            "In that case, you can choose between the salmon tatare and the cauliflower soup."
                        ),
                    ],
                    # TODO: Handle "nothing" condition
                ),
            ],
        ),
        Story(
            name="recommend_entree",
            elements=[
                action_ask_entree,
                Or(
                    intent_what_do_you_recommend,
                    intent_not_sure,
                    IntentName("help"),
                ),
                Utterance(
                    "I personally prefer the steak. Would you like that?"
                ),
                Fork(
                    [
                        Or(intent_sure_ill_get_that, IntentName("affirm")),
                        Utterance("Great, one steak then."),
                        # TODO: Set slot
                        ActionName("action_set_entree_steak"),
                    ],
                    [
                        IntentName("deny"),
                        Utterance(
                            "In that case, you can choose between the sea bass and the vegetarian lasagna."
                        ),
                    ],
                    # TODO: Handle "nothing" condition
                ),
            ],
        ),
    ],
    domain_filename="domain/restaurant/recommendations.yaml",
    nlu_filename="data/restaurant/recommendations.yaml",
    use_rules=False,
)
