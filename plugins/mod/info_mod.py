## This module returns information about the current channel/stream (ex: playlist, elo, etc)
## Name of the module, to be returned in desc()
name = "info_mod.py"


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    global send_message_function
    send_message_function = send_message_callback


## This function is called any time the bot receives input
def send_input(inp, sender, channel):
    if sender == 'riotgradius':
        send_message_function(channel, "You said: " + inp)


def execute(args_list, channel):
    send_message_function(channel, "Executing command.")

## Returns a description of the module including the name at the top
def desc():
    return name + ": gives various bits of information."


def teardown():
    print "This is the teardown function run when a plugin is removed"

