from libs.permissions import Permissions
import random

## Name of the module, to be returned in desc()
name = "game_signup.py"
users = []
cooldown = []
perm = Permissions()

## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    print "Example plugin running."
    global send_message_function
    send_message_function = send_message_callback


## This function is called any time the bot receives input
def send_input(inp, sender, channel):
    global users
    global cooldown

    inp_list = inp.split()

    if inp_list[0] == '!signup':
        if sender not in users and sender not in cooldown:
            users.append(sender)
            cooldown.append(sender)

    if inp_list[0] == '!userlist' and perm.isMod(sender):
        if len(inp_list) == 1:
            send_message_function(channel, "In queue: " + str(users))
            send_message_function(channel, "On cooldown: " + str(cooldown))

        if len(inp_list) == 2:
            short_list = users[:int(inp_list[1])]
            users = users[int(inp_list[1]):]
            send_message_function(channel, str(short_list))

        if len(inp_list) == 3:
            if inp_list[1] == 'r':
                short_list = random.sample(users, int(inp_list[2]))
                users = [x for x in users if x not in short_list]
                send_message_function(channel, str(short_list))

    if inp_list[0] == '!cooldown' and perm.isMod(sender):
        cooldown = []


## Returns a description of the module including the name at the top
def desc():
    return name + ": tracks users that run the !signup command to sign up for games."


def teardown():
    print "This is the teardown function run when a plugin is removed"