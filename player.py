# Import external libraries.
import json
import config

# The object model for the player character.
class Player:
    # These values are default placeholders. They will be overwritten when the player's data can be retrieved.

    # The player's name. Defined at the start of a new game.
    name = ""

    # The player's location.
    location = config.location_id_downtown

    # The player's amount of slimes.
    slimes = 0

    # The player's hunger.
    hunger = 0

    # Scenes are scripted sequences the player enter into for key moments in the story where normal commands are disabled.
    scene = None

    # The player's debt.
    debt = config.initial_debt

    # Create the player object.
    def __init__(self):
        # Open up the save file.
        with open('save.json', 'r') as save_file:
            # Turn the JSON object into a Python list containing dictionaries.
            data = json.load(save_file)

            # Retrieves the data from the first item in the list.
            player_data = data['player']

            # Loads the data into the player object.
            self.name = player_data['name']
            self.location = player_data['location']
            self.slimes = player_data['slimes']
            self.hunger = player_data['hunger']
            self.scene = player_data['scene']
            self.debt = player_data['debt']

            # Safely close the file.
            save_file.close()

    # Save the data from this player object to the save file.
    def persist(self):
        # Open up the save file again to store the data as a local dictionary for ease of use.
        with open('save.json', 'r') as save_file:
            # Turn the JSON object into a Python list containing dictionaries.
            save_data = json.load(save_file)
            # Safely close the file.
            save_file.close()

        # Update the save file.
        with open('save.json', 'w') as save_file:
            # Overwrite the save file with the data from this object.
            save_data['player']['name'] = self.name
            save_data['player']['location'] = self.location
            save_data['player']['slimes'] = self.slimes
            save_data['player']['hunger'] = self.hunger
            save_data['player']['scene'] = self.scene
            save_data['player']['debt'] = self.debt

            # Convert the dictionary into a JSON object and save it in a save file.
            json.dump(save_data, save_file, indent=2)

            # Safely close the file.
            save_file.close()
