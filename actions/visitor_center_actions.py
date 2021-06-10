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


class ActionResetTourSlots(ActionResetSlots):
    action_name = "action_reset_citypass_slots"
    slot_names = ["citypass_num_tickets", "citypass_confirmed"]


class ActionSetObjectAttribute(ActionSetSlot):
    slot_name = "object_attribute"


class ActionSetObjectAttributePrice(ActionSetObjectAttribute):
    action_name = "action_set_object_attribute_price"
    slot_value = "price"


class ActionSetObjectAttributeDuration(ActionSetObjectAttribute):
    action_name = "action_set_object_attribute_duration"
    slot_value = "duration"


class ActionSetObjectAttributeHours(ActionSetObjectAttribute):
    action_name = "action_set_object_attribute_hours"
    slot_value = "hours"


class ActionSetObjectAttributeDirections(ActionSetObjectAttribute):
    action_name = "action_set_object_attribute_directions"
    slot_value = "directions"


class ActionSetObjectAttributeDetails(ActionSetObjectAttribute):
    action_name = "action_set_object_attribute_details"
    slot_value = "details"
