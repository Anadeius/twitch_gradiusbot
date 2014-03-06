#TODO: Find a way to work around the circular dependency when adding the first Mod, maybe use config?

from libs.permissions import Permissions

## Name of the module, to be returned in desc()
name = "perms_plugin.py"
permissions = Permissions()


## What the module should return when processing text from IRC
## Gets inp from IRC, processes it, and returns the
def buildup(send_message_callback):
    print "Loading permissions helper."
    global send_message_function
    send_message_function = send_message_callback


def send_input(inp, sender, channel):

    try:
        arg_list = inp.split()

        if arg_list[0] == "@addtag" and permissions.has_tag(sender, 'mod'):
            permissions.add_tag(arg_list[1], arg_list[2])
            send_message_function(channel, "Added " + str(arg_list[2]) + " to " + arg_list[1] + " tags.")

        if arg_list[0] == "@remtag" and permissions.has_tag(sender, 'mod'):
            permissions.rem_tag(arg_list[1], arg_list[2])
            send_message_function(channel, "Removed " + str(arg_list[2]) + " from " + arg_list[1] + " tags.")

        if arg_list[0] == "@hastag" and permissions.has_tag(sender, 'mod'):
            send_message_function(channel, str(arg_list[1]) + " has " + str(arg_list[2]) + ": "
                                           + permissions.has_tag(arg_list[1], arg_list[2]))

        if arg_list[0] == "@listtags" and permissions.has_tag(sender, 'mod'):
            send_message_function(channel, str(permissions.list_tags(arg_list[1])))
    except:
        print "Something broke in perms_plugin.py"


def execute(args_list, channel):
    send_message_function(channel, "I have nothing to execute.")


## Returns a description of the module including the name at the top
def desc():
    return "Module name" + name + "Example Description"


def teardown():
    print "Removing permissions plugin."
