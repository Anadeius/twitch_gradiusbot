import pymongo
import sys
import ConfigParser


class ChatRpg():

    def __init__(self, config_file):
        #Parse Configuration File
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.max_start_stats = config.getint('Settings', 'max_start_stats')

        client = pymongo.MongoClient()
        rpg_db = client.rpg_db
        self.characters = rpg_db.characters
        self.inventory = rpg_db.inventory
        self.stats = rpg_db.stats

    def generate_character(self, char_name, in_str, in_vit):
        s_str = int(in_str)
        s_vit = int(in_vit)

        try:
            if (s_str + s_vit == self.max_start_stats) and (self.characters.find({"name": char_name}).count() == 0):
                hp = s_vit * 5
                char_post = {"name": char_name, "level": 1, "xp": 0, "hp": hp, "str": s_str, "vit": s_vit, "gold": 0}
                self.characters.insert(char_post)
                return "Character created successfully!"
            else:
                if self.characters.find({"name":char_name}).count() > 0:
                    return "Character already exists."
                if not (s_str + s_vit == self.max_start_stats):
                    return "Stats do not add up to " + str(self.max_start_stats) + "."

        except:
            print "Error generating character: ", sys.exc_info()

    def run_adventure(self):
        print

    def run_combat(self):
        print

    def gen_item(self):
        print

    def save_character(self):
        print

    def export_character_sheet(self):
        print