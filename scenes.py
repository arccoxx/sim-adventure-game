import player
import utilities
import config


def Introduction(message):
    save = utilities.Save()

    scene_progress = save.data['quest_progress'][config.scene_id_newgame]

    if scene_progress == 0:
        save.data['quest_progress'][config.scene_id_newgame] = 1
        save.persist()

        response = "You are in dire straits.<br><br>After being laid off unexpectedly last month, you have been trying to find new work to no avail. You have recently turned to mining slime to feed your family. For obvious reasons, mining slime is illegal. Your goal is to mine and sell as much of your slime as possible before getting caught by the authorities."
        response += "<br><br>But, first things firsts. What's your name?"
    elif scene_progress == 1:
        save.data['quest_progress'][config.scene_id_newgame] = 2
        save.persist()

        player_data = player.Player()
        player_data.name = message
        player_data.scene = None
        player_data.persist()
        response = "Understood. So, {player_name}, what will you do now?".format(player_name = player_data.name)
    return response
