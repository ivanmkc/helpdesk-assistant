from data_generation.models.object_models import Concept


class Type:
    place = Concept(name="place", synonyms=["location",],)

    place_of_worship = Concept(
        name="place of worship",
        synonyms=[
            "church",
            "monastery",
            "cathedral",
            "house of god",
            "temple",
            "shrine",
        ],
    )

    museum = Concept("museum", synonyms=["museum", "menagerie",],)

    art_gallery = Concept(
        "art gallery", synonyms=["gallery", "art show", "art museum",],
    )

    restaurant = Concept(
        "restaurant",
        synonyms=[
            "cafe",
            "food truck",
            "bistro",
            "cafeteria",
            "lunch room",
            "diner",
            "food court",
            "fast food",
            "eatery",
            "canteen",
            "snackbar",
            "beer garden",
            "coffee shop",
        ],
    )

    ticket = Concept(name="ticket", synonyms=["token", "coupon"],)

    tour = Concept(name="tour", synonyms=["trip", "safari"],)
