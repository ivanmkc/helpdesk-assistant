from typing import List, Optional, Union

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
        intro: Action,
        question_intent: Optional[Intent] = None,
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
        self.question_intent = question_intent
        self.intro = intro
        self.hours = hours
        self.more_details = more_details
        self.price = price
        self.duration = duration
        self.directions = directions
        self.related_actions = related_actions

    @staticmethod
    def _create_stories(
        entity_name: str,
        entity_synonyms: str,
        intents_or_utterances_with_context: List[Union[Intent, Utterance]],
        parameterized_intent_creator: ParameterizedIntentCreator,
        response_action: Action,
        question_intent: Optional[Intent] = None,
    ) -> List[Story]:
        stories: List[Story] = []
        if question_intent:
            stories.append(
                Story(
                    [
                        OrActions(*intents_or_utterances_with_context),
                        question_intent,
                        response_action,
                    ]
                )
            )

            stories.append(
                Story(
                    [
                        question_intent,
                        SlotWasSet(
                            slot_name=CONTEXT_SLOT_NAME, slot_value=entity_name
                        ),
                        response_action,
                    ]
                )
            )

        # TODO: Set context for utterances

        stories.append(
            Story(
                [
                    parameterized_intent_creator.create_parameterized_intent(
                        context_name=CONTEXT_SLOT_NAME,
                        context_value=entity_name,
                        context_value_synonyms=entity_synonyms,
                    ),
                    SlotWasSet(
                        slot_name=CONTEXT_SLOT_NAME, slot_value=entity_name
                    ),
                    response_action,
                ]
            )
        )

        # Return stories that aren't None
        return stories

    def generate_stories(self) -> List[Story]:
        # Consolidate all utterances
        # TODO: Replace by setting the context after each of these utterances
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
        if self.question_intent:
            all_stories.append(
                Story(
                    elements=[
                        self.question_intent,
                        self.intro,
                    ],
                )
            )

        all_stories.extend(
            self._create_stories(
                entity_name=self.name,
                entity_synonyms=self.synonyms,
                intents_or_utterances_with_context=utterances,
                parameterized_intent_creator=parameterized_intents.intent_is_there_a_context_creator,
                response_action=self.intro,
            )
        )

        if self.hours:
            all_stories.extend(
                self._create_stories(
                    entity_name=self.name,
                    entity_synonyms=self.synonyms,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_when_is_that_creator,
                    response_action=self.hours,
                    question_intent=common.intent_when_is_that,
                )
            )

        if self.price:
            all_stories.extend(
                self._create_stories(
                    entity_name=self.name,
                    entity_synonyms=self.synonyms,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_what_price_creator,
                    response_action=self.price,
                    question_intent=common.intent_what_price,
                )
            )

        if self.more_details:
            all_stories.extend(
                self._create_stories(
                    entity_name=self.name,
                    entity_synonyms=self.synonyms,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_what_is_context_creator,
                    response_action=self.more_details,
                    question_intent=common.intent_what_is_that,
                )
            )

        if self.duration:
            all_stories.extend(
                self._create_stories(
                    entity_name=self.name,
                    entity_synonyms=self.synonyms,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_what_duration_creator,
                    response_action=self.duration,
                    question_intent=common.intent_how_long,
                )
            )

        if self.directions:
            all_stories.extend(
                self._create_stories(
                    entity_name=self.name,
                    entity_synonyms=self.synonyms,
                    intents_or_utterances_with_context=utterances,
                    parameterized_intent_creator=parameterized_intents.intent_directions_creator,
                    response_action=self.directions,
                    question_intent=common.intent_directions,
                )
            )

        return [story for story in all_stories if story is not None]
