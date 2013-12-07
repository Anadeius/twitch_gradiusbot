import pymongo
import random
import sys
import ConfigParser


class ChatRpg():

    def __init__(self, config_file):
        #Parse Configuration File
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.max_start_stats = config.getint('Settings', 'max_start_stats')
        self.hit_mod = config.getfloat('Settings', 'hit_mod')

        client = pymongo.MongoClient()
        rpg_db = client.rpg_db
        self.characters = rpg_db.characters
        self.inventory = rpg_db.inventory
        self.stats = rpg_db.stats

    def generate_character(self, char_name, in_str, in_vit, in_dex, in_agi):
        s_str = int(in_str)
        s_vit = int(in_vit)
        s_dex = int(in_dex)
        s_agi = int(in_agi)

        try:
            if (s_str + s_vit + s_dex + s_agi == self.max_start_stats) and (self.characters.find({"name": char_name}).count() == 0):
                hp = s_vit * 5
                char_post = {"name": char_name, "level": 1, "xp": 0, "hp": hp, "str": s_str, "vit": s_vit, "agi": s_agi, "dex": s_dex, "gold": 0}
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
        try:
            print
        except:
            print "Error generating character: ", sys.exc_info()

    def run_combat(self, name1, name2):
        try:
            hp1, str1, vit1 = self.characters.find_one({"name": name1})["hp"], self.characters.find_one({"name": name1})["str"], self.characters.find_one({"name": name1})["vit"]
            agi1, dex1 = self.characters.find_one({"name": name1})["agi"], self.characters.find_one({"name": name1})["dex"]
            hp2, str2, vit2 = self.characters.find_one({"name": name2})["hp"], self.characters.find_one({"name": name2})["str"], self.characters.find_one({"name": name2})["vit"]
            agi2, dex2 = self.characters.find_one({"name": name2})["agi"], self.characters.find_one({"name": name2})["dex"]

            if agi1 >= agi2:
                turn = 1
            else:
                turn = 2

            while hp1 > 0 and hp2 > 0:
                if turn == 1:
                    hit_chance1 = (dex1 * self.hit_mod) / agi2
                    if random.random() < hit_chance1:
                        print name1 + " hit " + name2 + " with " + str(str1) + " damage!"
                        hp2 -= str1
                    else:
                        print name1 + " missed " + name2 + "!"
                    turn = 2
                elif turn == 2:
                    hit_chance2 = (dex2 * self.hit_mod) / agi1
                    if random.random() < hit_chance2:
                        print name2 + " hit " + name1 + " with " + str(str2) + " damage!"
                        hp1 -= str2
                    else:
                        print name2 + " missed " + name1 + "!"
                    turn = 1
            if hp1 > hp2:
                print name1 + " has beaten " + name2 + " in combat!"
                return name1
            else:
                print name2 + " has beaten " + name1 + " in combat!"
                return name2

        except:
            print "Error running combat: ", sys.exc_info()

    def gen_item(self):
        print

    def gen_creature(self, difficulty):
        print

    def save_character(self):
        print

    def export_character_sheet(self):
        print