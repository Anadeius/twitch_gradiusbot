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
    s_post = {"name": "status", "asked": False, "loop": False, "loop_count": 0, "answer": ""}
    status.insert(s_post)

def send_input(inp, sender, channel):
    if inp == "trivia" and data["asked"] == "false" and perm.isMod(sender):
        trivia_question(channel)

    if data["asked"] == "true":
        trivia_answer(channel,inp,sender)

    if len(inp.split()) == 2 and inp.split()[0] == "trivia" and perm.isMod(sender):
        send_message_function(channel,"Starting a trivia loop of " + inp.split()[1] + " questions.")
        data["loop"] = "true"
        # THIS VVV MATCHES THIS ^^^^, CHANGE ALL OTHERS
        status.update({"name":"status"}, {"$set": {"loop": True}})
        data["loop_count"] = str(int(inp.split()[1]) - 1)
        trivia_question(channel)

def desc():
    return ""

def teardown():
    print "Removing the Trivia module."

def trivia_question(channel):
    ans = ""

    if data["asked"] == "false":
        try:
            data["answer"] = s[1]
            ans = s[0].encode('ascii', 'ignore')
            data["asked"] = "true"
            temp.save_temp(t_file, data)
        except:
            print "Error generating question:", sys.exc_info()

        send_message_function(channel,ans)

def trivia_answer(channel,message,sender):
    if str.lower(message) == str.lower(str(data['answer'])):
        data["asked"] = "false"
        temp.save_temp(t_file, data)
        send_message_function(channel,"You are correct " + sender + "!")
        sb.addPoints(sender, 10)

        if data["loop"] == "true" and int(data["loop_count"]) == 0:
            data["loop"] = "false"
            send_message_function(channel,"I'm done with my trivia spree now.")
            temp.save_temp(t_file, data)

        if data["loop"] == "true" and int(data["loop_count"]) != 0:
            data["loop_count"] = str(int(data["loop_count"]) - 1)
            temp.save_temp(t_file, data)
            trivia_question(channel)
