import random

## Name of the module, to be returned in desc()
name = "buttreplacer.py"


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    print "Example plugin running."
    global send_message_function
    send_message_function = send_message_callback


## This function is called any time the bot receives input
def send_input(inp, sender, channel):
    butt_percent = 10

    if random.randint(0, 100) <= butt_percent:
        string_list = inp.split()
        target = random.choice(string_list)
        target_index = string_list.index(target)
        string_list[target_index] = 'butt'

        new_string = ' '.join(string_list)
        send_message_function(channel, sender + ", I think you meant: \"" + new_string + "\"")



def execute(args_list, channel):
    send_message_function(channel, "I don't execute anything.")


## Returns a description of the module including the name at the top
def desc():
    return name + ": is an example plugin."


def teardown():
    print "This is the teardown function run when a plugin is removed"
