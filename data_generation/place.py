from typing import Optional
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    TextSlot,
    BooleanSlot,
    ActionName,
    Action,
)

from typing import Any, Dict, List, Set
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
    ActionName,
)

import data_generation.common_intents as common

from data_generation.story_generation import Story, OrActions


class Place:
    def __init__(
        self,
        name: str,
        intent: Intent,
        intro: Action,
        synonyms: List[str] = [],
        hours: Optional[Action] = None,
        more_details: Optional[Action] = None,
        price: Optional[Action] = None,
        duration: Optional[Action] = None,
        directions: Optional[Action] = None,
        related_actions: List[Action] = [],
    ):
        self.name = name
        self.synonyms = synonyms
        self.intent = intent
        self.intro = intro
        self.hours = hours
        self.more_details = more_details
        self.price = price
        self.duration = duration
        self.directions = directions
        self.related_actions = related_actions

    def generate_nlu() -> Dict:
        pass

    def generate_stories(self) -> List[Story]:
        utterances = [
            utterance
            for utterance in [
                self.intro,
                self.hours,
                self.more_details,
                self.price,
                self.directions,
            ]
            + self.related_actions
            if utterance is not None
        ]

        story_intro = Story(
            elements=[
                self.intent,
                self.intro,
            ],
        )

        # TODO: Build intents using replacements

        story_hours = None
        if self.hours:
            story_hours = Story(
                [
                    OrActions(*utterances),
                    common.intent_when_is_that,
                    self.hours,
                ]
            )

        story_price = None
        if self.price:
            story_price = Story(
                [
                    OrActions(*utterances),
                    common.intent_what_price,
                    self.price,
                ]
            )

        story_details = None
        if self.more_details:
            story_details = Story(
                [
                    OrActions(*utterances),
                    common.intent_what_is_that,
                    self.more_details,
                ]
            )

        story_duration = None
        if self.duration:
            story_duration = Story(
                [
                    OrActions(*utterances),
                    common.intent_how_long,
                    self.duration,
                ]
            )

        story_directions = None
        if self.directions:
            story_directions = Story(
                [
                    OrActions(*utterances),
                    common.intent_directions,
                    self.directions,
                ]
            )

        return [
            story
            for story in [
                story_intro,
                story_hours,
                story_price,
                story_duration,
                story_details,
                story_directions,
            ]
            if story is not None
        ]
