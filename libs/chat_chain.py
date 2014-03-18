from pymongo import MongoClient
import sys
import traceback
import ConfigParser

class ChatChain():

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('libs/configs/chat_chain.cfg')

        #Get config values
        addr = config.get('ChatChain', 'addr')
        port = config.getint('ChatChain', 'port')
        user = config.get('ChatChain', 'user')
        passwd = config.get('ChatChain', 'passwd')

        try:
            uri = "mongodb://" + user + ":" + passwd + "@" + addr + ":" + str(port) + "/chatchain"
            mongo_client = MongoClient(uri)
            self.chain = mongo_client.gradiuscoin

        except:
            print "Failed to connect to database: " + str(sys.exc_info()[:2]) + traceback.format_exc()

    def seed_data_from_reddit(self, subreddit, count):
        print