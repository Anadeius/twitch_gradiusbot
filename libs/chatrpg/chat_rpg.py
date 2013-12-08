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
        self.enemies = rpg_db.enemies
        self.inventory = rpg_db.inventory
        self.stats = rpg_db.stats

    def fill_enemy_db(self, count):
        self.enemies.remove()
        for x in range(0, count):
            self.gen_creature(count)

    def gen_creature(self, difficulty):
        total_points = difficulty
        nouns = open("data/nouns.txt").read().splitlines()
        adj = open("data/adjectives.txt").read().splitlines()
        name = random.choice(adj) + " " + random.choice(nouns)
        attr = [1, 1, 1, 1]
        while total_points != 0:
            for x in range(0, len(attr)):
                num = random.randint(0, total_points)
                attr[x] = attr[x] + num
                total_points -= num
        e_str, e_vit, e_agi, e_dex = attr
        e_hp = e_vit * 5
        char_post = {"name": name, "level": 1, "xp": 0, "hp": e_hp, "str": e_str, "vit": e_vit, "agi": e_agi, "dex": e_dex, "gold": 0}
        self.enemies.insert(char_post)
        print "Enemy generated."

    def gen_item(self):
        print

    def generate_character(self, char_name, in_str, in_vit, in_dex, in_agi):
        s_str = int(in_str)
        s_vit = int(in_vit)
        s_dex = int(in_dex)
        s_agi = int(in_agi)

        try:
            if (s_str + s_vit + s_dex + s_agi == self.max_start_stats) and (self.characters.find({"name": char_name}).count() == 0):
                (s_str, s_vit, s_dex, s_agi) = (s_str+1, s_vit+1, s_dex+1, s_agi+1)
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

    def get_stats(self, name, db):
        hp1, str1, vit1 = db.find_one({"name": name})["hp"], db.find_one({"name": name})["str"], db.find_one({"name": name})["vit"]
        agi1, dex1 = db.find_one({"name": name})["agi"], db.find_one({"name": name})["dex"]
        return hp1, str1, vit1, agi1, dex1

    def run_adventure(self):
        try:
            ind = random.randint(0, self.enemies.count())
            enemy = self.enemies.find()[ind]['name']
            ind = random.randint(0, self.enemies.count())
            enemy2 = self.enemies.find()[ind]['name']
            self.run_combat(enemy, 'e', enemy2, 'e')

        except:
            print "Error running adventure: ", sys.exc_info()

    def run_combat(self, name1, type1, name2, type2):
        if type1 == 'e':
            db1 = self.enemies
        else:
            db1 = self.characters
        if type2 == 'e':
            db2 = self.enemies
        else:
            db2 = self.characters

        try:
            hp1, str1, vit1, agi1, dex1 = self.get_stats(name1, db1)
            hp2, str2, vit2, agi2, dex2 = self.get_stats(name2, db2)

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

    def save_character(self):
        print