import data_generation.visitor_center.book_tour.state_book_tour as state_book_tour
import data_generation.visitor_center.book_tour.stories_book_tour as stories_book_tour
import data_generation.visitor_center.buy_citypass.state_buy_citypass as state_buy_citypass
import data_generation.visitor_center.places_visitor_center as places_visitor_center
import data_generation.visitor_center.state_visitor_center as state_visitor_center
import data_generation.visitor_center.stories_visitor_center as stories_visitor_center
from data_generation import state_machine_generation, story_generation

domain_folder = "domain/visitor_center/"
nlu_folder = "data/visitor_center/"

domain_filename = "domain/visitor_center/stories.yaml"
nlu_filename = "data/visitor_center/stories.yaml"

# Start state
state_machine_generation.persist(
    state=state_visitor_center.start_state,
    is_initial_state=True,
    domain_folder=domain_folder,
    nlu_folder=nlu_folder,
)

# Buy CityPass state
state_machine_generation.persist(
    state=state_buy_citypass.buy_citypass_state,
    is_initial_state=False,
    domain_folder=domain_folder,
    nlu_folder=nlu_folder,
)

# Book tour state
state_machine_generation.persist(
    state=state_book_tour.book_tour_state,
    is_initial_state=False,
    domain_folder=domain_folder,
    nlu_folder=nlu_folder,
)

# Stories
story_generation.persist(
    stories_visitor_center.stories_tell_me_more
    + stories_book_tour.stories_tours
    + stories_visitor_center.stories_what_time
    + [
        story
        for place in places_visitor_center.places
        for story in place.generate_stories()
    ],
    domain_filename=domain_filename,
    nlu_filename=nlu_filename,
    use_rules=False,
)
