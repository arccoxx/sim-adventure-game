# Import external libraries.
import re

# Import other parts of our code.
import config
import commands
import config

# Map of all commands and their functions.
command_map = {
    config.command_help: commands.help,
    config.command_debug: commands.debug,
    config.command_exit: commands.exit,
    config.command_mine: commands.mine,
    config.command_data: commands.data,
    config.command_move: commands.move,
    config.command_look: commands.look,
}

# When we input a message, check to see if it's a valid command and then execute it if it is.
async def on_message(message):
    # Tokenize the message. The command should be the first word.
    tokens = message.split(' ')

    # Check how many tokens there are.
    tokens_count = len(tokens)

    # If there's at least one token, define the command used as the first item in the tokens list.
    command = tokens[0].lower() if tokens_count > 0 else None

    # Create command object for your command.
    command_object = commands.Command(
        tokens = tokens,
        message = message,
    )

    # Check the main command map for the requested command.
    global command_map
    command_found = command_map.get(command)

    if command_found is not None:
        # Execute found command.
        return await command_found(command_object)

    else: # Could not find the inputted command.
        response = "That is not a valid command."
        await send_message(format_message(response))

# Format message.
def format_message(message, new_prompt = True):
    return "\n{}\n>".format(message)

# Convert the response spit out by commands into an input or prints it if no new prompt is required.
async def send_message(response, new_prompt = True):
    if new_prompt is True:
        new_command = input(response)
        await on_message(new_command)

    else:
        print(response)

#Turn an array of tokens into a single word (no spaces or punctuation) with all lowercase letters.
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

