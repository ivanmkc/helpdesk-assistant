from typing import Any, Dict, List, Set

from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    Slot,
    TextSlot,
    BooleanSlot,
)

from rasa.shared.nlu.state_machine.state_machine_state import (
    Action,
    Response,
    StateMachineState,
    Transition,
)

from rasa.shared.nlu.state_machine.conditions import (
    AndCondition,
    IntentCondition,
    OnEntryCondition,
    SlotEqualsCondition,
    SlotsFilledCondition,
)

from data_generation import state_machine_generation

# class SpaceEntity(Enum, Entity):
#     person = "PERSON"
#     geopolitical_entity = "GPE"
#     location = "LOC"

#     def name(self) -> str:
#         return self.value

# Tasks
# Leave without paying
# Get the waiter angry
# Compliment the waiter
# Get the waiter to tell you a secret
# Book a date for your anniversary dinner


wantToLeaveIntent = Intent(name="want_to_leave", examples=["I want to leave"])

whereAreYouFromIntent = Intent(
    name="where_are_you_from", examples=["Where are you from?"]
)

wheresTheWashroomIntent = Intent(
    name="wheres_the_washroom",
    examples=[
        "Where's the washroom?",
        "Where is the restroom?",
        "What is the location of the washroom?",
        "I need to find the toilet",
    ],
)

howAreYouDoingIntent = Intent(
    name="how_are_you_doing", examples=["How are you doing?"]
)

select_salad = Intent(
    name="select_salad",
    examples=[
        "I'll have the salad",
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

slot_appetizer = TextSlot(
    name="appetizer",
    intents={
        select_salad: "salad",
        select_soup: "soup",
        select_tatare: "tatare",
    },
    prompt_actions=[
        Utterance("What would you like for your appetizer?"),
    ],
)

slot_entree = TextSlot(
    name="entree",
    intents={
        select_fish: "fish",
        select_steak: "steak",
        select_vegetables: "lasagna",
    },
    prompt_actions=[
        Utterance("What would you like for your entree?"),
    ],
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
    condition=SlotsFilledCondition([slot_appetizer, slot_entree]),
    intents={
        "affirm": True,
        "deny": False,
    },
    prompt_actions=[
        Utterance(
            "Okay, just to confirm. For your appetizer, you'll have the {appetizer} and for your entree, you'll have the {entree}. Is that correct?"
        ),
    ],
)


# generalResponses: List[Response] = [
#     Response(
#         condition=IntentCondition(whereAreYouFromIntent),
#         actions=[
#             Utterance(text="I'm from Canada", name="utter_where_from_response")
#         ],
#     ),
#     Response(
#         condition=IntentCondition(wheresTheWashroomIntent),
#         actions=[
#             Utterance(
#                 text="It's in the cafeteria",
#                 name="utter_washroom_response",
#             )
#         ],
#     ),
#     Response(
#         condition=IntentCondition(howAreYouDoingIntent),
#         actions=[
#             Utterance(
#                 text="I'm doing great",
#                 name="utter_how_are_you_response",
#             )
#         ],
#     ),
#     Response(
#         condition=IntentCondition(
#             Intent(
#                 name="what_are_hours",
#                 examples=[
#                     "What are your hours?",
#                     "When do you close?",
#                     "What time do you open until?",
#                     "What time do you close?",
#                     "Are you still open?",
#                 ],
#             )
#         ),
#         actions=[
#             Utterance(
#                 text="We're open from 9 to 5, Mondays to Fridays.",
#                 name="utter_hours",
#             )
#         ],
#     ),
#     Response(
#         condition=IntentCondition(
#             Intent(
#                 examples=[
#                     "Are you busy?",
#                     "How busy are you?",
#                     "Do you have a lot of work?",
#                 ],
#             )
#         ),
#         actions=[
#             Utterance(
#                 text="It's not too busy around here as you can see.",
#             )
#         ],
#     ),
#     Response(
#         condition=IntentCondition(
#             Intent(
#                 name="what_school_mascot",
#                 examples=[
#                     "What's the school mascot?",
#                 ],
#             )
#         ),
#         actions=[
#             Utterance(
#                 text="Why, the stag of course",
#             ),
#             Utterance(
#                 text="The school mascot? You must mean the stag",
#             ),
#         ],
#     ),
# ]

# TODO: Add a drink


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
        Utterance("I really like how they make the {entree} here."),
        Utterance(
            text="Great choices. The {appetizer} goes great with the {entree}"
        ),
    ],
    transitions=[
        Transition(
            name="leave",
            condition=IntentCondition(wantToLeaveIntent),
            transition_utterances=[
                Utterance(
                    text="I guess you can leave if you need to, since we haven't made the food yet.",
                    name="utter_leave_response",
                )
            ],
            destination_state=None,
        )
    ],
    responses=[
        Response(
            condition=OnEntryCondition(),
            actions=[
                Utterance("Welcome to Michi Cafe"),
                Utterance(
                    "Here is your menu. I'll be back in 5 minutes for your order."
                ),
                Utterance("Okay, hope you've looked at the menu."),
            ],
        ),
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
                    "Okay great, please enjoy yourself while the food is readied."
                ),
                # SetSlotsAction(
                #     [slot_appetizer, slot_entree, slot_order_confirmed]
                # ),
            ],
        ),
    ],
)

state_machine_generation.persist(
    student_life_state_machine,
    states_filename="state_machines/restaurant/ordering.yaml",
    domain_filename="domain/restaurant/ordering.yaml",
    nlu_filename="data/restaurant/ordering.yaml",
)
