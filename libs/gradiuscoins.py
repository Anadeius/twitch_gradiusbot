from pymongo import MongoClient
import ConfigParser
import sys
import traceback


class GradiusCoins():

    def __init__(self):
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
            self.gc_db = mongo_client.gradiuscoin

        except:
            print "Failed to connect to database: " + str(sys.exc_info()[:2]) + traceback.format_exc()

    def get_coins(self, target):
        curr_wallet = 0

        if self.gc_db.wallet.find({"nick": target}).count() > 0:
            curr_wallet = float(self.gc_db.wallet.find({"nick": target})[0]['gc'])

        return curr_wallet

    def give_coins(self, target, amount):
        if self.gc_db.wallet.find({"nick": target}).count() > 0:
            curr_wallet = self.get_coins(target)
            curr_wallet += amount
            self.gc_db.wallet.update({"nick": target}, {'$set': {'gc': curr_wallet}})
        else:
            self.gc_db.wallet.insert({"nick": target, "gc": amount})

    def take_coins(self, target, amount):
        success = False

        if self.gc_db.wallet.find({"nick": target}).count() > 0:
            curr_wallet = self.get_coins(target)

            if curr_wallet >= amount:
                self.give_coins(target, amount*-1)
                success = True

        return success

    def trade_coins(self, target1, target2, amount):
        success = False

        t1_wallet = self.get_coins(target1)

        if t1_wallet >= amount:
            self.give_coins(target2, amount)
            success = True

        return success