## This is an example file for how all IRC modules should be

import time
import random
## Name of the module, to be returned in desc()
name = "Example.py"

## What the module should return when processing text from IRC
## Gets inp from IRC, processes it, and returns the
def buildup(send_message_callback):
    print "This function is run at creation of the plugin"
    global send_message_function
    send_message_function = send_message_callback

def send_input(inp, sender, channel):
    if sender == "riotgradius":
        send_message_function(channel,"I'm a bot...")
        time.sleep(5)
        send_message_function(channel,"And this is my message...")
        time.sleep(5)
        send_message_function(channel,"But this is just a test.")

## Returns a description of the module including the name at the top
def desc():
    return "Module name" + name + "Example Description"

def teardown():
    print "This function is run at removal of the plugin"

