from dataclasses import dataclass, field
from typing import Optional, List
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
)

import abc


@dataclass
class Concept:
    name: str
    synonyms: List[str]


@dataclass
class Object(abc.ABC, Concept):
    @abc.abstractproperty
    def type(self) -> str:
        pass

    intro: str
    question_intent: Optional[Intent] = None
    activities_provided: List[Concept] = field(default_factory=list)
    things_provided: List[Concept] = field(default_factory=list)


@dataclass
class Place(Object):
    intro: str
    question_intent: Optional[Intent] = None
    activities_provided: List[Concept] = field(default_factory=list)
    things_provided: List[Concept] = field(default_factory=list)
    hours: Optional[str] = None
    more_details: Optional[str] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    directions: Optional[str] = None
    related_actions: List[str] = field(default_factory=list)

    @property
    def type(self) -> str:
        return "place"
