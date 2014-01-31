# twitch_gradiusbot

A bot for moderating twitch chat.  Can load python code that fits the plugin standard without having to restart the bot, as well as reload code that was changed without a restart.

## Submitting Code
Please help if you would like to.  I try and stick to the PEP8 standards as much as possible, so I'd appreciate it if you do the same.  I'll review the code and merge it if all is good.  A good way to figure out what might be needed is to look at the issues list.


## Plugins

Example plugin:

```python
## This is an example file for how all IRC modules should be

## Name of the module, to be returned in desc()
name = "Example.py"


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    print "Example plugin running."
    global send_message_function
    send_message_function = send_message_callback


## This function is called any time the bot receives input
def send_input(inp, sender, channel):
    send_message_function(channel, "Example message.")


## Returns a description of the module including the name at the top
def desc():
    return name + ": is an example plugin."


def teardown():
    print "This is the teardown function run when a plugin is removed"
```

Each plugin is ran in a different thread. This may or may not cause race conditions based on your code.  It's still a little buggy.
