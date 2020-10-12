# WARNING. THIS FILE IS VERY, VERY MESSY. DON'T WORRY ABOUT TRYING TO UNDERSTAND IT UNTIL I STREAMLINE IT AND COMMENT EVERYTHING IN A LATER PATCH.
# WARNING. THIS FILE IS VERY, VERY MESSY. DON'T WORRY ABOUT TRYING TO UNDERSTAND IT UNTIL I STREAMLINE IT AND COMMENT EVERYTHING IN A LATER PATCH.
# WARNING. THIS FILE IS VERY, VERY MESSY. DON'T WORRY ABOUT TRYING TO UNDERSTAND IT UNTIL I STREAMLINE IT AND COMMENT EVERYTHING IN A LATER PATCH.

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

        def __init__(self, id = "", alias = [], name = "", description = "", neighbors = None):
            self.id = id
            self.alias = alias
            self.name = name
            self.description = description
            self.neighbors = neighbors

# Directions and cost from the player's current location to arrive at their destination.
class Path:
    visited = None
    steps = None
    cost = 0
    iters = 0
    locations_visited = None

    def __init__(
        self,
        path_from = None,
        steps = [],
        cost = 0,
        visited = {},
        locations_visited = None
    ):
        if path_from != None:
            self.steps = deepcopy(path_from.steps)
            self.cost = path_from.cost
            self.visited = deepcopy(path_from.visited)
            self.locations_visited = deepcopy(path_from.locations_visited)
        else:
            self.steps = steps
            self.cost = cost
            self.visited = visited
            if locations_visited == None:
                self.locations_visited = set()
            else:
                self.locations_visited = locations_visited

def path_to(location_start = None, location_end = None, player_data = None,):
    score_golf = math.inf
    score_map = {}
    
    for location in config.locations_list:
        score_map[location.id] = math.inf

    paths_finished = []
    paths_walking = []

    locations_adjacent = []

    location_start = config.id_to_location.get(location_start)
    location_end = config.id_to_location.get(location_end)

    path_base = Path(
        steps = [location_start],
        cost = 0,
        locations_visited = set([location_start.id]),
    )

    path_id = 0
    heapq.heappush(paths_walking, (path_base.cost + landmark_heuristic(path_base, location_end), path_id, path_base))
    path_id += 1

    count_iter = 0
    
    while len(paths_walking) > 0:
        count_iter += 1

        path_tuple = heapq.heappop(paths_walking)

        path = path_tuple[-1]

        if path is not None:
            step_last = path.steps[-1]
            score_current = score_map.get(step_last.id)
            if path.cost >= score_current:
                continue

            score_map[step_last.id] = path.cost

            step_penult = path.steps[-2] if len(path.steps) >= 2 else None

            if location_end != None:
                if step_last.id == location_end.id:
                    path_final = path
                    if path_final.cost < score_golf:
                        score_golf = path_final.cost
                        paths_finished = []
                    if path_final.cost <= score_golf:
                        paths_finished.append(path_final)
                    break

            else:
                location_adjacent = step_last

                if location_adjacent.id != location_start.id:

                    locations_adjacent.append(location_adjacent)
                    continue

            path_base = path
            neighs = list(step_last.neighbors.keys())
            
            if step_penult != None and step_penult.id in neighs:
                neighs.remove(step_penult.id)

            num_neighbors = len(neighs)
            i = 0
            for i in range(num_neighbors):

                neigh = config.id_to_location.get(neighs[i])
                neigh_cost = step_last.neighbors.get(neigh.id)
                    
                if neigh_cost == None:
                    continue

                if i < num_neighbors - 1:
                    branch = path_branch(path_base, neigh, neigh_cost, player_data, location_end)
                    if branch != None:
                        heapq.heappush(paths_walking, (branch.cost + landmark_heuristic(branch, location_end), path_id, branch))
                        path_id += 1
                else:
                    if path_step(path_base, neigh, neigh_cost, player_data, location_end):
                        heapq.heappush(paths_walking, (path_base.cost + landmark_heuristic(path_base, location_end), path_id, path_base))
                        path_id += 1

    if location_end != None:
        path_true = None
        if len(paths_finished) > 0:
            path_true = paths_finished[0]
            path_true.iters = count_iter
        if path_true is None:
            print("Could not find a path.")
        return path_true
    else:
        return locations_adjacent

# Add location_next to the path.
def path_step(path, location_next, cost_next, player_data, location_end, landmark_mode = False):

    next_location = location_next

    if not location_next.id in path.locations_visited:
        path.locations_visited.add(next_location.id)

    path.steps.append(location_next)

    path.cost += cost_next

    return True

# Returns a new path including all of path_base, with the next step location_next.
def path_branch(path_base, location_next, cost_next, player_data, location_end, landmark_mode = False):
    path_next = Path(path_from = path_base)

    if path_step(path_next, location_next, cost_next, player_data, location_end, landmark_mode) == False:
        return None
    
    return path_next

def score_map_from(location_start = None, player_data = None, landmark_mode = False):
    score_golf = math.inf
    score_map = {}
    for location in config.locations_list:
        score_map[location.id] = score_golf

    paths_walking = []

    location_start = config.id_to_location.get(location_start)
    location_end = None
    location_end = None

    path_base = Path(
        steps = [ location_start ],
        cost = 0,
        locations_visited = set([location_start.id]),
    )

    paths_walking.append(path_base)

    count_iter = 0
    while len(paths_walking) > 0:
        count_iter += 1

        paths_walking_new = []

        for path in paths_walking:
            step_last = path.steps[-1]
            score_current = score_map.get(step_last.id)
            if path.cost >= score_current:
                continue

            score_map[step_last.id] = path.cost

            step_penult = path.steps[-2] if len(path.steps) >= 2 else None

            path_base = path
            neighs = list(step_last.neighbors.keys())

            if step_penult != None and step_penult.id in neighs:
                neighs.remove(step_penult.id)

            num_neighbors = len(neighs)
            for i in range(num_neighbors):

                neigh = config.id_to_location.get(neighs[i])
                neigh_cost = step_last.neighbors.get(neigh.id)

                if neigh_cost == None:
                    continue

                if i < num_neighbors - 1:
                    branch = path_branch(path_base, neigh, neigh_cost, player_data, location_end, landmark_mode)
                    if branch != None:
                        paths_walking_new.append(branch)

                else:
                    if path_step(path_base, neigh, neigh_cost, player_data, location_end, landmark_mode):
                        paths_walking_new.append(path_base)

        paths_walking = paths_walking_new

    return score_map

landmarks = {}

def landmark_heuristic(path, location_end):
	if len(landmarks) == 0 or location_end is None:
		return 0
	else:
		last_step = path.steps[-1]
		scores = []
		for lm in landmarks:
			score_map = landmarks.get(lm)
			score_path = score_map.get(last_step.id)
			score_goal = score_map.get(location_end.id)
			scores.append(abs(score_path - score_goal))

		return max(scores)