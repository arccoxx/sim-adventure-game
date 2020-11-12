import player
import utilities
import config


def Introduction(message):
    save = utilities.Save()

    scene_progress = save.data['quest_progress'][config.scene_id_newgame]

    if scene_progress == 0:
        save.data['quest_progress'][config.scene_id_newgame] = 1
        save.persist()

        response = "You are in dire straits.<br><br>After being laid off unexpectedly last month, you have been trying to find new work to no avail. In your desperation, you turned to one of the city's notorious loan sharks for help. Your family was fed for a few months, but.. now you're {:,} slimes in debt and still without a job. In order to pay off your loan, you'll have to mine some slime in one of the quarries in the outskirts of the city. It might be illegal, and it might be horribly demeaning, but you don't have any other choice.".format(config.initial_debt)
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
