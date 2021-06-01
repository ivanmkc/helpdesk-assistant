import uuid
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import rasa.shared.constants
import rasa.shared.utils.validation
from rasa.shared.core.domain import Domain
from rasa.shared.core.slots import (
    AnySlot,
    BooleanSlot,
    CategoricalSlot,
    FloatSlot,
    ListSlot,
    Slot,
    TextSlot,
)
from rasa.shared.nlu.state_machine.state_machine_models import (
    Intent,
    Utterance,
)
from rasa.shared.nlu.state_machine.state_machine_state import Action
from rasa.shared.nlu.state_machine.yaml_convertible import StoryYAMLConvertable
from rasa.shared.nlu.training_data.formats import RasaYAMLReader
from rasa.shared.utils.io import dump_obj_as_yaml_to_string, write_text_file


class IntentName(StoryYAMLConvertable):
    name: str

    def __init__(self, name: str):
        self.name = name

    def as_story_yaml(self) -> Dict:
        return {"intent": self.name}


class SlotWasSet(StoryYAMLConvertable):
    def __init__(self, slot_name: str, slot_value: Optional[Any]) -> None:
        self.slot_name = slot_name
        self.slot_value = slot_value

    def as_story_yaml(self) -> Dict:
        return {
            "slot_was_set": [
                {self.slot_name: self.slot_value}
                if self.slot_value is not None
                else self.slot_value
            ]
        }


class Or(StoryYAMLConvertable):
    intents: List[Union[Intent, IntentName]]

    def __init__(self, *args: Union["Or", Intent]) -> None:
        intents = list(args)

        if all(
            [
                isinstance(intent, Intent) or isinstance(intent, IntentName)
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
    paths: List[Union["Or", Intent, Action, IntentName, SlotWasSet]]
    name: str

    def __init__(
        self,
        elements: Union["Or", Intent, Action, Fork, SlotWasSet],
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
        # all_slots: Set[Slot] = []

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
                    assert isinstance(last_element, Utterance)
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
            intents=[intent.name for intent in all_intents],
            entities=[
                entity for intent in all_intents for entity in intent.entities
            ],  # List of entity names
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


def persist(
    stories: List[Story],
    domain_filename: str,
    nlu_filename: str,
    use_rules: bool = False,
):
    all_domain = Domain.empty()
    all_intents: Set[Intent] = set()
    all_stories: List[Story] = []
    all_slot_was_sets: Set[SlotWasSet] = set()

    for story in stories:
        domain, stories, intents, slot_was_sets = story.get_domain_nlu(
            use_rules=use_rules
        )

        all_domain = all_domain.merge(domain)
        all_intents.update(intents)
        all_stories.extend(stories)
        all_slot_was_sets.update(slot_was_sets)

    # Go through all entities and create consolidated slot
    slots_dict: Dict[str, List[Any]] = {}
    for slot_was_set in all_slot_was_sets:
        new_slot_values = slots_dict.get(slot_was_set.slot_name, []) + [
            slot_was_set.slot_value
        ]
        slots_dict[slot_was_set.slot_name] = list(
            set(new_slot_values)
        )  # Get unique values

    slots: List[Slot] = [
        CategoricalSlot(name=slot_name, values=slot_values)
        for slot_name, slot_values in slots_dict.items()
    ]

    # Append consolidated slots
    domain_slots = Domain(
        intents=[],
        entities=[],
        slots=slots,
        responses={},
        action_names=[],
        forms=[],
    )
    all_domain = all_domain.merge(domain_slots)

    # Validate domain
    rasa.shared.utils.validation.validate_yaml_schema(
        all_domain.as_yaml(), rasa.shared.constants.DOMAIN_SCHEMA_FILE
    )

    # Write domain
    all_domain.persist(domain_filename)

    # Write NLU
    nlu_data = {
        "version": "2.0",
        "nlu": [intent.as_nlu_yaml() for intent in all_intents],
        "rules" if use_rules else "stories": all_stories,
    }

    nlu_data_yaml = dump_obj_as_yaml_to_string(
        nlu_data, should_preserve_key_order=True
    )

    RasaYAMLReader().validate(nlu_data_yaml)

    # TODO: Create folders if not existent

    write_text_file(nlu_data_yaml, nlu_filename)
