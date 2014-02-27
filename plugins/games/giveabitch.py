## This is an example file for how all IRC modules should be

import random
## Name of the module, to be returned in desc()
name = "giveabitch.py"

vowels = set('aeiou')

## What the module should return when processing text from IRC
## Gets inp from IRC, processes it, and returns the
def buildup(send_message_callback):
    print "We gonna tell dem what to give bitches."
    global send_message_function
    send_message_function = send_message_callback


def send_input(inp,sender,channel):

    words = [line.strip() for line in open('plugins/data/items.dic')]
    gift = random.choice(words).upper()
    
    plural = pluralize(gift).upper()
    
    if gift[0] in vowels:
        gift = 'N ' + gift
    else:
        gift = ' ' + gift
    
    if ("what do you give a bitch?" in inp.lower()):
        send_message_function(channel,'GIVE THAT BITCH A' + gift + '. BITCHES LOVE ' + plural + '.')


def execute(args_list, channel):
    send_message_function(channel, "I have nothing to execute.")


## Returns a description of the module including the name at the top
def desc():
    return name + ":Tells you what to give a bitch."


def pluralize(singular):
    root = singular
    try:
        if singular[-1] == 'y' and singular[-2] not in vowels:
            root = singular[:-1]
            suffix = 'ies'
        elif singular[-1] == 's':
            if singular[-2] in vowels:
                if singular[-3:] == 'ius':
                    root = singular[:-2]
                    suffix = 'i'
                else:
                    root = singular[:-1]
                    suffix = 'ses'
            else:
                suffix = 'es'
        elif singular[-2:] in ('ch', 'sh'):
            suffix = 'es'
        else:
            suffix = 's'
    except IndexError:
        suffix = 's'
    plural = root + suffix
    return plural


def teardown():
    print "No more telling them what to give bitches."
