# Import external libraries.
import json
import config

# The object model for the player character.
class Player:
    # These values are default placeholders.
    # The player's name. Defined at the start of a new game.
    name = ""

    # The player's location.
    location = config.location_downtown

    # The player's amount of slimes.
    slimes = 0

    # This is used to determine if the player has a previous save file upon start up.
    # It is always initally defined as True, before being redefined as False if a save file is found and data is retrieved.
    new_game = True
    
    # Create the player object.
    def __init__(self):
        try: # Search for a save file. If no error is thrown, retrieve the data from it.
            with open('save.json') as save_file:
                # Turn the JSON object into a Python list containing dictonaries.
                data = json.load(save_file)
                
                # Retrieves the data from the first item in the list.
                player_data = data[0] 

                # Loads the data into the player object. 
                self.name = player_data['name']
                self.location = player_data['location']
                self.slimes = player_data['slimes']

                # Safely close the file.
                save_file.close()

                # Makes it known that this player object used loaded data from a save file.
                self.new_game = False    


        except: # If no save file was found, or if an error was thrown while retreiveing the data, create a new save file.
            with open('save.json', 'w') as save_file:
                # Create a new dictonary containing the default Player class values.
                player_data = {
                    "name": self.name,
                    "location": self.location,
                    "slimes": self.slimes
                },

                # Convert the new dictonary into a JSON object and save it in a new save file.             
                json.dump(player_data, save_file, indent = 2)
                
                # Safely close the file.
                save_file.close()

    # Save the data from this player object to the save file.
    def persist(self):
        with open('save.json', 'w') as save_file:
            # Create a dictonary containing the current values from this player object.
            player_data = {
                "name": self.name,
                "location": self.location,
                "slimes": self.slimes
            },

            # Convert the dictonary into a JSON object and save it in a save file.            
            json.dump(player_data, save_file, indent = 2)
            
            # Safely close the file.
            save_file.close()
        
