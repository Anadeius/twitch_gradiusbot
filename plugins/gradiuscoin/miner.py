from pymongo import MongoClient
import ConfigParser
import traceback
import sys
import time

## Name of the module, to be returned in desc()
name = "miner.py"


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    global send_message_function
    global gc_db

    config = ConfigParser.RawConfigParser()
    config.read('plugins/gradiuscoin/gradiuscoin.cfg')

    #Get config values
    addr = config.get('Miner', 'addr')
    port = config.getint('Miner', 'port')
    user = config.get('Miner', 'user')
    passwd = config.get('Miner', 'passwd')


    try:
        uri = "mongodb://" + user + ":" + passwd + "@" + addr + ":" + str(port) + "/gradiuscoin"
        mongo_client = MongoClient(uri)
        gc_db = mongo_client.gradiuscoin

    except:
        print "Failed to connect to database: " + str(sys.exc_info()[:2]) + traceback.format_exc()

    send_message_function = send_message_callback

## This function is called any time the bot receives input
def run(channel):
    while True:
        print "I'm looping because I'm cool."
        time.sleep(5)

def send_input(inp,sender,channel):
    print "This is running and I dont know why."

## Returns a description of the module including the name at the top
def desc():
    return name + ": is an example plugin."


def teardown():
    print "This is the teardown function run when a plugin is removed"
