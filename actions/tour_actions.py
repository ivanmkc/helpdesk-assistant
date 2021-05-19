from actions.action_set_slot import ActionSetSlot
from actions.action_reset_slots import ActionResetSlots


class ActionSetTourBus(ActionSetSlot):
    action_name = "action_set_tour_bus"
    slot_name = "tour_type"
    slot_value = "bus"


class ActionSetTourBoat(ActionSetSlot):
    action_name = "action_set_tour_boat"
    slot_name = "tour_type"
    slot_value = "boat"


class ActionResetTourSlots(ActionResetSlots):
    action_name = "action_reset_tour_slots"
    slot_names = ["tour_type", "tour_num_tickets", "tour_confirmed"]
