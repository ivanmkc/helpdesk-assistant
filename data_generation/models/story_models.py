import uuid
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from rasa.shared.core.domain import Domain
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)
from rasa.shared.nlu.state_machine.state_machine_state import Action
from rasa.shared.nlu.state_machine.yaml_convertible import StoryYAMLConvertable


class Checkpoint(StoryYAMLConvertable):
    def __init__(self, name: str) -> None:
        self.name = name

    def as_story_yaml(self) -> Dict:
        return {"checkpoint": self.name}


class SlotWasSet(StoryYAMLConvertable):
    def __init__(
        self, slots_and_values: List[Union[Dict[str, Any], str]]
    ) -> None:
        self.slots_and_values = slots_and_values

    def as_story_yaml(self) -> Dict:
        return {"slot_was_set": self.slots_and_values}


class Or(StoryYAMLConvertable):
    intents: List[Union[Intent, Intent]]

    def __init__(self, *args: Union["Or", Intent]) -> None:
        intents = list(args)

        if all(
            [
                isinstance(intent, Intent) or isinstance(intent, Intent)
                for intent in intents
            ]
        ):
            self.intents = intents
        else:
            raise TypeError("Non-intent detected")

    def all_intents(self) -> Set[Intent]:
        return set(
            [intent for intent in self.intents if isinstance(intent, Intent)]
        )

    def as_story_yaml(self) -> Dict:
        return {"or": [intent.as_story_yaml() for intent in self.intents]}


class OrActions(StoryYAMLConvertable):
    actions: List[Union[Action]]

    def __init__(self, *args: Union[Action]) -> None:
        actions = list(args)

        if all([isinstance(action, Action) for action in actions]):
            self.actions = actions
        else:
            raise TypeError("Non-action detected")

    def as_story_yaml(self) -> Dict:
        return {}


class Fork(StoryYAMLConvertable):
    paths: List[List[Union["Or", Intent, Action, "Fork"]]]

    def __init__(
        self, *args: List[Union["Or", Intent, Action, "Fork"]]
    ) -> None:
        self.paths = list(args)

    def as_story_yaml(self) -> Dict:
        return {}


class Story:
    paths: List[Union["Or", Intent, Action, Intent, SlotWasSet]]
    name: str

    def __init__(
        self,
        elements: List[Union["Or", Intent, Action, Fork, SlotWasSet]],
        name: Optional[str] = None,
    ) -> None:
        self.paths = elements
        self.name = name or str(uuid.uuid4())

        # Only the last element may be a fork
        for element in elements[:-1]:
            assert not isinstance(element, Fork)

    def get_domain_nlu(
        self, use_rules: bool
    ) -> Tuple[Domain, List[Dict], Set[Intent]]:
        story_nlu_steps: List[str] = []
        last_element: Optional[Intent] = None

        sub_domains: List[Domain] = []
        sub_nlus: List[Dict] = []

        all_intents: Set[Intent] = set()
        all_utterances: Set[Utterance] = set()
        all_actions: Set[Action] = set()
        all_slot_was_sets: Set[SlotWasSet] = set()

        for element_index, element in enumerate(self.paths):
            # Add to current story
            story_nlu_steps.append(element.as_story_yaml())

            if isinstance(element, Intent):
                all_intents.add(element)
            elif isinstance(element, Utterance):
                all_utterances.add(element)
            elif isinstance(element, Or):
                all_intents.update(element.all_intents())
            elif isinstance(element, Action):
                all_actions.add(element)
            elif isinstance(element, SlotWasSet):
                all_slot_was_sets.add(element)
            elif isinstance(element, OrActions):
                # Start a new story for every fork
                for action_index, action in enumerate(element.actions):
                    story = Story(
                        name=f"{self.name}_action_fork_{action_index}",
                        elements=[action] + self.paths[element_index + 1 :],
                    )

                    (
                        sub_domain,
                        sub_nlu,
                        sub_intents,
                        sub_slot_was_sets,
                    ) = story.get_domain_nlu(use_rules=use_rules)
                    sub_domains.append(sub_domain)
                    sub_nlus += sub_nlu
                    all_intents.update(sub_intents)
                    all_slot_was_sets.update(sub_slot_was_sets)

                # All subsequent elements have been accounted for, so break
                break
            elif isinstance(element, Fork):
                if last_element:
                    assert isinstance(last_element, Action)
                else:
                    assert RuntimeError(
                        "Fork must not be the first element in a story path."
                    )

                # Start a new story for every fork
                for index, path in enumerate(element.paths):
                    story = Story(
                        name=f"{self.name}_fork_{index}",
                        elements=[last_element] + path,
                    )

                    (
                        sub_domain,
                        sub_nlu,
                        sub_intents,
                        sub_slot_was_sets,
                    ) = story.get_domain_nlu(use_rules=use_rules)
                    sub_domains.append(sub_domain)
                    sub_nlus += sub_nlu
                    all_intents.update(sub_intents)
                    all_slot_was_sets.update(sub_slot_was_sets)

                if element_index != len(self.paths) - 1:
                    raise ValueError(
                        "The fork must be the last element of its path."
                    )

            last_element = element

        # Filter out empty dictionaries
        story_nlu_steps = [step for step in story_nlu_steps if bool(step)]

        # Persist domain
        domain = Domain(
            intents=list({intent.name for intent in all_intents}),
            entities=list(
                {
                    entity
                    for intent in all_intents
                    for entity in intent.entities
                }
            ),  # List of entity names
            slots=[],
            responses={
                utterance.name: [{"text": utterance.text}]
                for utterance in all_utterances
            },
            action_names=[action.name for action in all_actions],
            forms={},
            action_texts=[],
        )

        # Merge sub-domains
        for sub_domain in sub_domains:
            domain = domain.merge(sub_domain)

        # Save current story
        story_nlu = (
            [
                {
                    "rule" if use_rules else "story": self.name,
                    "steps": story_nlu_steps,
                }
            ]
            if len(story_nlu_steps)
            > 1  # Omit all stories with less than 2 steps
            else []
        )
        story_nlu += sub_nlus

        # wait_for_user_input
        if use_rules:
            for nlu in story_nlu:
                nlu["wait_for_user_input"] = False

        return (domain, story_nlu, all_intents, all_slot_was_sets)
