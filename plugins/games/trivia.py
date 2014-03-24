from libs.permissions import Permissions
from libs.temp_pickle import TempPickle
from libs.gradiuscoins import GradiusCoins
from pymongo import MongoClient
import sys
import traceback
import random

perms = Permissions()
tp = TempPickle()
gc = GradiusCoins()

## Name of the module, to be returned in desc()
name = "trivia.py"
tmp_file = 'plugins/data/tmp/trivia.tmp'


## This is ran at the initial import of the plugin.
## send_message_function is a callback function to send a message back to the IRC channel
def buildup(send_message_callback):
    print "Trivia plugin running."
    global send_message_function
    global trivia_db
    send_message_function = send_message_callback

    trivia_tmp = tp.load(tmp_file)
    trivia_tmp['asked'] = False
    tp.save(trivia_tmp, tmp_file)

    user = 'user'
    passwd = 'password123'
    addr = 'localhost'
    port = '27017'

    try:
        uri = "mongodb://" + user + ":" + passwd + "@" + addr + ":" + str(port) + "/trivia"
        mongo_client = MongoClient(uri)
        trivia_db = mongo_client.trivia

    except:
        print "Failed to connect to database: " + str(sys.exc_info()[:2]) + traceback.format_exc()


## This function is called any time the bot receives input
def send_input(inp, sender, channel):
    trivia_tmp = tp.load(tmp_file)
    isplit = inp.split()

    if perms.has_tag(sender, 'trivia') and isplit[0] == '!trivia' and len(isplit) == 3:
        trivia_tmp['num_questions'] = int(isplit[1])
        trivia_tmp['topic'] = isplit[2]
        tp.save(trivia_tmp, tmp_file)
        ask_trivia(channel, isplit[2])

    if trivia_tmp['asked']:
        if inp.lower() == trivia_tmp['answer']:
            trivia_tmp['num_questions'] -= 1
            send_message_function(channel, "That is correct, " + sender + "!")
            gc.give_coins(sender, 10)
            trivia_tmp['asked'] = False
            tp.save(trivia_tmp, tmp_file)

            if trivia_tmp['num_questions'] > 0:
                ask_trivia(channel, trivia_tmp['topic'])


def execute(args_list, channel):
    send_message_function(channel, "Executing command.")


## Returns a description of the module including the name at the top
def desc():
    return name + ": is an example plugin."


def teardown():
    print "Removing Trivia plugin"


def ask_trivia(channel, topic):
    topics = {'lol': trivia_db.lol, 'stream': trivia_db.stream}

    if topic not in topics.keys() or topic == 'all':
        topic = random.choice(topics.keys())

    trivia_tmp = tp.load(tmp_file)
    trivia_tmp['asked'] = True

    ind = random.randint(0, topics[topic].count()-1)
    answer = str(topics[topic].find()[ind]["answer"])
    question = str(topics[topic].find()[ind]["question"])
    trivia_tmp['answer'] = answer.lower()
    tp.save(trivia_tmp, tmp_file)
    print "[DEBUG]: Answer is - " + repr(answer)
    send_message_function(channel, question)