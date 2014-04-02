from pymongo import MongoClient
from libs.permissions import Permissions
import ConfigParser
import traceback
import sys
import time
import pickle
import os

## Name of the module, to be returned in desc()
name = "miner.py"

perm = Permissions()

## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    global send_message_function
    global mine_freq
    global mine_rate
    global gc_per_mine
    global tmp_file
    global gc_db
    global perm

    config = ConfigParser.RawConfigParser()
    config.read('plugins/gradiuscoin/gradiuscoin.cfg')

    #Get config values
    addr = config.get('Miner', 'addr')
    port = config.getint('Miner', 'port')
    user = config.get('Miner', 'user')
    passwd = config.get('Miner', 'passwd')
    tmp_file = config.get('Miner', 'tmp_file')

    #Get Miner specific config values
    mine_rate = config.getfloat('Miner', 'mine_rate')
    gc_per_mine = config.getint('Miner', 'gc_per_mine')
    mine_freq = config.getint('Miner', 'mine_freq')

    #Ensure the tmp file exists
    if not os.path.isfile(tmp_file):
        miner_tmp = {}
        miner_tmp['execute_loop'] = True
        pickle.dump(miner_tmp, open(tmp_file, "wb"))

    else:
        miner_tmp = load(tmp_file)
        miner_tmp['execute_loop'] = True
        pickle.dump(miner_tmp, open(tmp_file, "wb"))

    try:
        uri = "mongodb://" + user + ":" + passwd + "@" + addr + ":" + str(port) + "/gradiuscoin"
        mongo_client = MongoClient(uri)
        gc_db = mongo_client.gradiuscoin

    except:
        print "Failed to connect to database: " + str(sys.exc_info()[:2]) + traceback.format_exc()

    send_message_function = send_message_callback


def execute(args_list, channel):
    send_message_function(channel, "Starting mining with: [mine_rate]=" + str(mine_rate) + " [gc_per_mine]="
                                   + str(gc_per_mine) + " [mine_freq]=" + str(mine_freq))

    #Load the dictionary file for tmp settings
    miner_tmp = load(tmp_file)
    miner_tmp['execute_loop'] = True

    while miner_tmp['execute_loop']:

        miner_tmp = pickle.load(open(tmp_file, "rb"))
        talked_list = []
        if gc_db.talkers.find().count() > 0:
            talked_list = gc_db.talkers.find()[0]['talkers']

        #print "[DEBUG] Granting " + str(talked_list) + " with " + str(mine_rate*gc_per_mine) + " gradiuscoins"
        for user in talked_list:
            if gc_db.wallet.find({"nick": user}).count() > 0:
                curr_wallet = float(gc_db.wallet.find({"nick": user})[0]['gc'])
                curr_wallet += gc_per_mine * mine_rate
                gc_db.wallet.update({"nick": user}, {'$set': {'gc': curr_wallet}})
            else:
                gc_db.wallet.insert({"nick": user, "gc": gc_per_mine * mine_rate})
        gc_db.talkers.remove()
        time.sleep(1)
        time.sleep(mine_freq)


## This function is called any time the bot receives input
def send_input(inp, sender, channel):

    #Check for chat commands
    if inp == '@stopmine' and perm.has_tag(sender, 'mod'):
        miner_tmp = pickle.load(open(tmp_file, "rb"))
        miner_tmp['execute_loop'] = False
        pickle.dump(miner_tmp, open(tmp_file, "wb"))

    #Mark those that talked in the talkers database
    if gc_db.talkers.find().count() > 0:
        talked_list = gc_db.talkers.find()[0]['talkers']

        if sender not in talked_list:
            talked_list.append(sender)
            talked_post = {"talkers": talked_list}
            gc_db.talkers.remove()
            gc_db.talkers.insert(talked_post)
    else:
        talked_post = {"talkers": [sender]}
        gc_db.talkers.remove()
        gc_db.talkers.insert(talked_post)


## Returns a description of the module including the name at the top
def desc():
    return name + ": is an example plugin."


def teardown():
    print "This is the teardown function run when a plugin is removed"


def save(perms, file_name):
    pickle.dump(perms, open(file_name, "wb"))


def load(file_name):
    return pickle.load(open(file_name, "rb"))
