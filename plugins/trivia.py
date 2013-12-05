import sys
import pymongo
import libs.load_temp as temp
from libs.permissions import Permissions
from libs.scoreboard import Scoreboard

name = "old_trivia.py"
t_file = "plugins/data/trivia.tmp"
data = temp.load_temp(t_file)
perm = Permissions()
sb = Scoreboard()
client = pymongo.MongoClient()
trivia_db = client.trivia_db
status = trivia_db.status
questions = trivia_db.questions


def buildup(send_message_callback):
    print "This function is run at buildup of function."
    global send_message_function
    send_message_function = send_message_callback
    s_post = {"name": "status", "asked": False, "loop": False, "loop_count": 0, "answer": "", "question": ""}
    status.insert(s_post)


def send_input(inp, sender, channel):
    if inp == "trivia" and not status.find_one()["asked"] and perm.isMod(sender):
        trivia_question(channel)

    if status.find_one()["asked"]:
        trivia_answer(channel, inp, sender)

    if len(inp.split()) == 2 and inp.split()[0] == "trivia" and perm.isMod(sender):
        send_message_function(channel,"Starting a trivia loop of " + inp.split()[1] + " questions.")
        status.update({"name": "status"}, {"$set": {"loop": True}})
        status.update({"name": "status"}, {"$set": {"loop_count": str(int(inp.split()[1]) - 1)}})
        trivia_question(channel)


def desc():
    return ""


def teardown():
    print "Removing the Trivia module."


def trivia_question(channel):
    if not status.find_one()["asked"]:
        try:
            status.update({"name": "status"}, {"$set": {"answer": "bestanswer"}})
            status.update({"name": "status"}, {"$set": {"question": "bestquestion"}})
            status.update({"name": "status"}, {"$set": {"asked": True}})
        except:
            print "Error generating question:", sys.exc_info()

        send_message_function(channel, status.find_one()["question"])


def trivia_answer(channel, message, sender):
    if str.lower(message) == str.lower(str(data['answer'])):
        status.update({"name": "status"}, {"$set": {"asked": False}})
        send_message_function(channel,"You are correct " + sender + "!")
        sb.addPoints(sender, 10)

        if status.find_one()["loop"] and status.find_one()["loop_count"] == 0:
            status.update({"name": "status"}, {"$set": {"loop": False}})
            send_message_function(channel,"I'm done with my trivia spree now.")

        if status.find_one()["loop"] and status.find_one()["loop_count"] != 0:
            status.update({"name": "status"}, {"$set": {"loop_count": int(status.find_one()["loop_count"])}})
            trivia_question(channel)
