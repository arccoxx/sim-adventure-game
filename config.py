# Import other parts of our code.
from map import Location
from item import Item

game_name = "Untitled Text Adventure Game"
game_version = "0.2"

# Commands.
command_help = 'help'
command_debug = 'debug'
command_exit = 'exit'
command_mine = 'mine'
command_data = 'data'
command_move = 'move'
command_look = 'look'
command_create_item = 'create'
command_eat = 'eat'

# Variables for scenes.
scene_id_newgame = "Introduction"

# Generic responses.
text_invalid_location = "You must be in {location_name} to use this command."

# Generic inputs in the affirmative.
accept_inputs = [
	"yes",
	"okay",
	"accept",
]

# Generic inputs in the negative.
decline_inputs = [
	"no",
	"nah",
	"decline"
]

travel_time_default = 5

# Variables for the locations in the game.
location_id_downtown = "downtown"
location_id_suburbs = "suburbs"
location_id_the_mines = "themines"

# A list of every location in the game as Location objects.
location_list = [
	Location(
		id=location_id_downtown,
		alias=[
			"dt",
		],
		name="Downtown",
		description="This is Downtown.",
		neighbors={
			location_id_suburbs: travel_time_default,
		},
	),
	Location(
		id=location_id_suburbs,
		alias=[
			"s",
		],
		name="Suburbs",
		description="This is Suburbs.",
		neighbors={
			location_id_downtown: travel_time_default,
			location_id_the_mines: travel_time_default,
		},
	),
	Location(
		id=location_id_the_mines,
		alias=[
			"mines",
			"m"
		],
		name="the Mines",
		description="This is the Mines.",
		neighbors={
			location_id_suburbs: travel_time_default,
		},
	),
]

# A dictionary mapping every location identifier to their corresponding locations as Location objects.
id_to_location = {}

for location in location_list:
	# Populate the dictionary.
	id_to_location[location.id] = location

	# Connect the aliases of each location to their corresponding Location objects too.
	for alias in location.alias:
		id_to_location[alias] = location

item_list = [
	Item(
		id = "compass",
		name = "Compass",
		description = "This is a compass!",
	),
	Item(
		id = "diamond",
		name = "Diamond",
		description = "What a beautiful diamond!",
	),
	Item(
		id = "apple",
		name = "Red Apple",
		description = "Juicy and delicious...",
	),
]

# A dictionary mapping every item identifier to their corresponding items as Items objects.
item_map = {}

# Populate item map.
for item in item_list:
	item_map[item.id] = item