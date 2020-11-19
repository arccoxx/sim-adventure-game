# Import other parts of our code.
import config

# The object model for locations on the map.
class Location:
    # These values are default placeholders.

    # The unique identifier for this location. All lowercase, no spaces.
    id = ""

    # Acceptable alternative names for this place. All lowercase, no spaces.
    alias = []

    # The nice, proper name for this place. May contain uppercase letters, and spaces.
    name = ""

    # The description provided when looking while in the location.
    description = ""

    # A list of all locations the player can move to from this one.
    neighbors = None

    def __init__(self, id = "", alias = [], name = "", description = "", neighbors = None, vendors = []):
        self.id = id
        self.alias = alias
        self.name = name
        self.description = description
        self.neighbors = neighbors
