## Name of the module, to be returned in desc()
name = "chance_games.py"
import random
import sys
from libs.gradiuscoins import GradiusCoins


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    print "Chance games now running"
    global send_message_function
    global gc
    gc = GradiusCoins()
    send_message_function = send_message_callback


## This function is called any time the bot receives input
def send_input(inp, sender, channel):
    cmd = inp.split()[0]
    args = inp.split()[1:]

    """
    #Current Ideas:
    /roll game
    betting game - takes 3 people, two people to bet one manager
    pickpocket game - game of skill?
    """
    if cmd == "!gradiuscoins":
        gradiuscoins = gc.get_coins(sender)
        send_message_function(channel, "You have " + str(gradiuscoins) + " gradiuscoins " + sender + "!")

    if cmd == "!roll" and len(args) == 1:
        try:
            if float(args[0]) > 0:
                has_coins = gc.take_coins(sender, float(args[0]))

                if has_coins:
                    roll = random.randint(1, 100)

                    if roll <= 25:
                        send_message_function(channel, "You rolled " + str(roll) + ", so I get to keep your " + args[0] + " gradiuscoins.")

                    if 25 < roll <= 50:
                        gc.give_coins(sender, float(args[0]))
                        send_message_function(channel, "You rolled " + str(roll) + ", so you get your " + args[0] + " gradiuscoins back.")

                    elif 50 < roll <= 75:
                        coins = float(args[0]) * 1.5
                        gc.give_coins(sender, coins)
                        send_message_function(channel, "You rolled " + str(roll) + ", so you get " + str(coins) + " gradiuscoins!")

                    elif roll > 75:
                        coins = float(args[0]) * 3.0
                        gc.give_coins(sender, coins)
                        send_message_function(channel, "You rolled " + str(roll) + ", so you get " + str(coins) + " gradiuscoins!")
        except:
            print "Error running !roll:", sys.exc_info()

def execute(args_list, channel):
    send_message_function(channel, "Executing command.")


## Returns a description of the module including the name at the top
def desc():
    return name + ": is an example plugin."


def teardown():
    print "This is the teardown function run when a plugin is removed"

