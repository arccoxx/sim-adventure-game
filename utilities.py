# Import external libraries.
import re
import json
import pygame
import pygame_gui

# Import other parts of our code.
import config
import commands
import config

# Map of all commands and their functions.
command_map = {
    config.command_help: commands.help,
    config.command_debug: commands.debug,
    config.command_mine: commands.mine,
    config.command_data: commands.data,
    config.command_look: commands.look,
    config.command_move: commands.move,
    config.command_order: commands.order,
    config.command_eat: commands.eat,
    config.command_deposit: commands.deposit,
    config.command_menu: commands.menu,
    config.command_inventory: commands.inventory,
}

# When we input a message, check to see if it's a valid command and then execute it if it is.
def parse_message(message, output = None):
    # Tokenize the message. The command should be the first word.
    tokens = message.split(' ')

    # Check how many tokens there are.
    tokens_count = len(tokens)

    # If there's at least one token, define the command used as the first item in the tokens list.
    command = tokens[0].lower() if tokens_count > 0 else None

    # Create command object for your command.
    command_object = commands.Command(
        tokens=tokens,
        message=message,
    )

    # Check the main command map for the requested command.
    global command_map
    command_found = command_map.get(command)

    if command_found is not None:
        # Execute found command.
        return command_found(command_object)

    else:  # Could not find the inputted command.
        response = "That is not a valid command."
        return response

# Turn an array of tokens into a single word (no spaces or punctuation) with all lowercase letters.
def flattenTokens(tokens):
    flattener = re.compile("[ '\"!@#$%^&*().,/?{}\[\];:]")

    target_name = ""

    if type(tokens) == list:
        for token in tokens:
            target_name += flattener.sub("", token.lower())

    else:
        target_name = flattener.sub("", tokens.lower())

    return target_name


# Map of user IDs to their course ID.
moves_active = {}

class Save():
    data = None

    def __init__(self):
        try:  # Open the save file.
            with open('save.json', 'r') as save_file:
                save_data = json.load(save_file)
                save_file.close()
                self.data = save_data
        except:  # If there isn't a save file in the directory, create one.
            with open('save.json', 'w') as save_file:
                # Create the initial data structure of the save file and create in default values for every key.
                save_data = {
                    "player": {
                        "name": None,
                        "location": config.location_id_downtown,
                        "slimes": 0,
                        "hunger": 0,
                        "scene": config.scene_id_newgame,
                        "debt": config.initial_debt,
                    },
                    "quest_progress": {
                        config.scene_id_newgame: 0
                    },
                    "items": {},
                }

                # Convert the new dictionary into a JSON object and save it in a new save file.
                json.dump(save_data, save_file, indent=2)

                # Safely close the file.
                save_file.close()

                with open('save.json', 'r') as save_file:
                    save_data = json.load(save_file)
                    save_file.close()
                    self.data = save_data

    def persist(self):
        # Commit the new changes to the save file.
        with open('save.json', 'w') as save_file:
            # Convert the dictionary into a JSON object and save it in a save file.
            json.dump(self.data, save_file, indent=2)

            # Safely close the file.
            save_file.close()

def format_nice_list(names = [], conjunction = "and"):
	list = len(names)

	if list == 0:
		return ''

	if list == 1:
		return names[0]
	
	return ', '.join(names[0:-1]) + '{comma} {conj} '.format(comma = (',' if list > 2 else ''), conj = conjunction) + names[-1]

pygame.init()

screen_width = 896
screen_height = 504

screen = pygame.display.set_mode((screen_width, screen_height))

background_colour = pygame.Color("#808080")

ui_manager = pygame_gui.UIManager((screen_width, screen_height), "assets/ui_theme.json")
ui_manager.add_font_paths('jost', "assets/font.ttf")
ui_manager.preload_fonts([{'name': 'jost', 'point_size': 18, 'style': 'bold'},
                          {'name': 'jost', 'point_size': 18, 'style': 'italic'}])

def generate_command_line():
    player_text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect(
        (75, 440), (790, 50)), manager=ui_manager, object_id="#player_input")
    pygame_gui.elements.UILabel(pygame.Rect(
        (50, 428), (25, 50)), ">", manager=ui_manager, object_id="#carat")
    ui_manager.select_focus_element(player_text_entry)


def generate_output(response):
    return pygame_gui.elements.UITextBox(response, pygame.Rect((25, 25), (845, 380)), manager=ui_manager, object_id="#scene_text")
