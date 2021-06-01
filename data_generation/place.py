from typing import Any, Dict, List, Optional, Set, Union

from rasa.shared.nlu.state_machine.state_machine_models import (
    Action,
    ActionName,
    BooleanSlot,
    Intent,
    TextSlot,
    Utterance,
)

import data_generation.common_intents as common
import data_generation.parameterized_intents as parameterized_intents
from data_generation.parameterized_intents import ParameterizedIntentCreator
from data_generation.story_generation import OrActions, SlotWasSet, Story

CONTEXT_SLOT_NAME = "context"


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

    def _create_stories(
        self,
        element_name: str,
        intents_or_utterances_with_context: List[Union[Intent, Utterance]],
        parameterized_intent_creator: ParameterizedIntentCreator,
        question_intent: Intent,
        response_action: Action,
    ) -> Dict:
        story = Story(
            [
                OrActions(*intents_or_utterances_with_context),
                question_intent,
                response_action,
            ]
        )

        # TODO: Set context for utterances

        story_by_entities = Story(
            [
                parameterized_intent_creator.create_parameterized_intent(
                    context_entity_name=CONTEXT_SLOT_NAME,
                    context_value=element_name,
                ),
                SlotWasSet(
                    slot_name=CONTEXT_SLOT_NAME, slot_value=element_name
                ),
                response_action,
            ]
        )

        story_by_context = Story(
            [
                question_intent,
                SlotWasSet(
                    slot_name=CONTEXT_SLOT_NAME, slot_value=element_name
                ),
                response_action,
            ]
        )

        return [story, story_by_entities, story_by_context]

    def generate_stories(self) -> List[Story]:
        # Consolidate all utterances
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

        all_stories: List[Story] = []

        # Create intro story
        story_intro = Story(
            elements=[
                self.intent,
                self.intro,
            ],
        )
        all_stories.append(story_intro)

        if self.hours:
            all_stories.extend(
                self._create_stories(
                    element_name=self.name,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_when_is_that_creator,
                    question_intent=common.intent_when_is_that,
                    response_action=self.hours,
                )
            )

        if self.price:
            all_stories.extend(
                self._create_stories(
                    element_name=self.name,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_what_price_creator,
                    question_intent=common.intent_what_price,
                    response_action=self.price,
                )
            )

        if self.more_details:
            all_stories.extend(
                self._create_stories(
                    element_name=self.name,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_what_is_context_creator,
                    question_intent=common.intent_what_is_that,
                    response_action=self.more_details,
                )
            )

        if self.duration:
            all_stories.extend(
                self._create_stories(
                    element_name=self.name,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_what_duration_creator,
                    question_intent=common.intent_how_long,
                    response_action=self.duration,
                )
            )

        if self.directions:
            all_stories.extend(
                self._create_stories(
                    element_name=self.name,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_directions_creator,
                    question_intent=common.intent_directions,
                    response_action=self.directions,
                )
            )

        return [story for story in all_stories if story is not None]
