# Import other parts of our code.
import config
import commands

# Map of all commands and their functions.
command_map = {
	config.command_help: commands.help,
    config.command_debug: commands.debug,
    config.command_exit: commands.exit,
    config.command_mine: commands.mine,
    config.command_data: commands.data,
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
def format_message(message):
    return "\n{}\n>".format(message)

# Convert the response spit out by commands into an input.
async def send_message(response):
    new_command = input(response)

    await on_message(new_command)
