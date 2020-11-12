# Import external libraries.
import asyncio
import time
import math
import heapq
import random
from copy import deepcopy

# Import other parts of our code.
import config

# The object model for locations on the map.
class Location:
        # The unique, flattened identifier for this location. All lowercase, no spaces.
        id = ""

        # Acceptable alternative names for this place. All lowercase, no spaces.
        alias = []

        # The nice, proper name for this place. May contain uppercase letters, and spaces.
        name = ""

        # The description provided when looking at the location.
        description = ""

        # A dictonary that defines the travel time between adjacent locations. {location_id: int}
        neighbors = None

        vendors = []

        def __init__(self, id = "", alias = [], name = "", description = "", neighbors = None, vendors = []):
            self.id = id
            self.alias = alias
            self.name = name
            self.description = description
            self.neighbors = neighbors
            self.vendors = vendors
