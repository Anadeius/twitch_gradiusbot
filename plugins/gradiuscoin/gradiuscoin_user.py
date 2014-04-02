from libs.gradiuscoins import GradiusCoins
from libs.throttling import Throttling
import random
import sys

gc = GradiusCoins()
limit = Throttling()

## Name of the module, to be returned in desc()
name = "gradiuscoin_user.py"


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    print "Loading gradiuscoin_user plugin"
    global send_message_function
    send_message_function = send_message_callback
    limit.set_rate_limit('!wallet', 1, 1)
    limit.set_rate_limit('!give', 3, 30)
    limit.set_rate_limit('!settings', 1, 3600)
    limit.set_rate_limit('!help', 1, 1800)
    limit.set_rate_limit('!roll', 1, 1)


## This function is called any time the bot receives input
def send_input(inp, sender, channel):

    isplit = inp.split()

    if inp == '!wallet' and limit.can_use_command(sender, '!wallet'):
        gradiuscoins = gc.get_coins(sender)
        send_message_function(channel, "You have " + str(gradiuscoins) + " gradiuscoins " + sender + "!")

    if isplit[0] == '!give' and limit.can_use_command(sender, '!give') and len(isplit) == 3:
        success = gc.trade_coins(sender, isplit[1], int(isplit[2]))
        if success:
            send_message_function(channel, sender + " gave " + isplit[1] + " " + isplit[2] + " gradiuscoins!")

    if inp == '!help' and limit.can_use_command(sender, '!help'):
        send_message_function(channel, "You can find the commands here: https://github.com/gradiuscypher/twitch_gradiusbot/tree/master/plugins/gradiuscoin")

    if isplit[0] == '!roll' and limit.can_use_command(sender, '!roll'):
        try:
            if float(isplit[1]) > 0:
                has_coins = gc.take_coins(sender, float(isplit[1]))

                if has_coins:
                    roll = random.randint(1, 100)

                    if roll <= 25:
                        send_message_function(channel, "You rolled " + str(roll) + ", so I get to keep your " + isplit[1] + " gradiuscoins.")

                    if 25 < roll <= 50:
                        gc.give_coins(sender, float(isplit[1]))
                        send_message_function(channel, "You rolled " + str(roll) + ", so you get your " + isplit[1] + " gradiuscoins back.")

                    elif 50 < roll <= 75:
                        coins = float(isplit[1]) * 1.5
                        gc.give_coins(sender, coins)
                        send_message_function(channel, "You rolled " + str(roll) + ", so you get " + str(coins) + " gradiuscoins!")

                    elif roll > 75:
                        coins = float(isplit[1]) * 3.0
                        gc.give_coins(sender, coins)
                        send_message_function(channel, "You rolled " + str(roll) + ", so you get " + str(coins) + " gradiuscoins!")
        except:
            print "Error running !roll:", sys.exc_info()

def execute(args_list, channel):
    send_message_function(channel, "Executing command.")


## Returns a description of the module including the name at the top
def desc():
    return name + ": user commands for gradiuscoins."


def teardown():
    print "Removing gradiuscoin_user plugin."
