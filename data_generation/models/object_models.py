from dataclasses import dataclass, field
from typing import Optional, List
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Union,
    Utterance,
)

import abc


class Concept:
    def __init__(self, name: str, synonyms: List[str]):
        self.name = name
        self.synonyms = synonyms


@dataclass
class BuyInfo:
    slot_name: str
    number_slot_name: str
    trigger_name: str


class Object(abc.ABC, Concept):
    def __init__(
        self,
        name: str,
        synonyms: List[str],
        intro: Union[str, Utterance],
        question_intent: Optional[Intent] = None,
        buy_info: Optional[BuyInfo] = (None,),
        types: List[Concept] = [],
        activities_provided: List[Concept] = [],
        things_provided: List[Concept] = [],
    ):
        super().__init__(name=name, synonyms=synonyms)

        if isinstance(intro, str):
            self.intro = Utterance(intro)
        else:
            self.intro = intro

        self.question_intent = question_intent
        self.buy_info = buy_info
        self.types = types
        self.activities_provided = activities_provided
        self.things_provided = things_provided

    @property
    def utterances(self) -> List[Utterance]:
        return [self.intro]


class Place(Object):
    def __init__(
        self,
        name: str,
        synonyms: List[str],
        intro: Union[str, Utterance],
        question_intent: Optional[Intent] = None,
        buy_info: Optional[BuyInfo] = (None,),
        types: List[Concept] = [],
        activities_provided: List[Concept] = [],
        things_provided: List[Concept] = [],
        hours: Optional[Union[str, Utterance]] = None,
        details: Optional[Union[str, Utterance]] = None,
        price: Optional[Union[str, Utterance]] = None,
        duration: Optional[Union[str, Utterance]] = None,
        directions: Optional[Union[str, Utterance]] = None,
        opinion: Optional[Union[str, Utterance]] = None,
    ):
        super().__init__(
            name=name,
            synonyms=synonyms,
            intro=intro,
            question_intent=question_intent,
            buy_info=buy_info,
            types=types,
            activities_provided=activities_provided,
            things_provided=things_provided,
        )

        name_altered = "".join(
            e.lower()
            for e in name
            if e.isalnum() or e.isspace() or e in ["-", "_"]
        )
        name_altered = "_".join(name_altered.split(" "))

        if isinstance(hours, str):
            self.hours = Utterance(hours, name=f"utter_{name_altered}_hours")
        else:
            self.hours = hours

        if isinstance(details, str):
            self.details = Utterance(
                details, name=f"utter_{name_altered}_details"
            )
        else:
            self.details = details

        if isinstance(price, str):
            self.price = Utterance(price, name=f"utter_{name_altered}_price")
        else:
            self.price = price

        if isinstance(duration, str):
            self.duration = Utterance(
                duration, name=f"utter_{name_altered}_duration"
            )
        else:
            self.duration = duration

        if isinstance(directions, str):
            self.directions = Utterance(
                directions, name=f"utter_{name_altered}_directions"
            )
        else:
            self.directions = directions

        if isinstance(opinion, str):
            self.opinion = Utterance(
                opinion, name=f"utter_{name_altered}_opinion"
            )
        else:
            self.opinion = opinion

    @property
    def utterances(self) -> List[Utterance]:
        additional_utterances = [
            self.hours,
            self.details,
            self.price,
            self.directions,
            self.duration,
            self.opinion,
        ]

        return super().utterances + [
            utterance
            for utterance in additional_utterances
            if utterance is not None
        ]
