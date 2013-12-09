import pymongo
import paramiko
import random
import sys
import ConfigParser
import logging
import os
import shutil


class ChatRpg():

    def __init__(self, config_file):
        self.sys_log = logging.getLogger('system-log')
        sys_log_hndl = logging.FileHandler('logs/system_log.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        sys_log_hndl.setFormatter(formatter)
        self.sys_log.addHandler(sys_log_hndl)
        self.sys_log.setLevel(logging.DEBUG)

        #Parse Configuration File
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        self.max_start_stats = config.getint('Settings', 'max_start_stats')
        self.hit_mod = config.getfloat('Settings', 'hit_mod')
        self.xp_curve = config.getfloat('Settings', 'xp_curve')
        self.xp_mod = config.getfloat('Settings', 'xp_mod')
        self.scp_host = config.get('Settings', 'scp_host')
        self.scp_port = config.getint('Settings', 'scp_port')
        self.char_sheet_folder = config.get('Settings', 'char_sheet_folder')
        self.sftp_dir = config.get('Settings', 'sftp_dir')
        self.scp_user = config.get('Settings', 'scp_user')
        self.ssh_key = config.get('Settings', 'ssh_key')

        client = pymongo.MongoClient()
        rpg_db = client.rpg_db
        self.characters = rpg_db.characters
        self.enemies = rpg_db.enemies
        self.inventory = rpg_db.inventory
        self.stats = rpg_db.stats

    def allocate_stats(self, name, add_stats_array):
        current_stats = self.characters.find({'name': name})[0]['free_stats']
        cost = sum(add_stats_array)
        try:
            if cost <= current_stats and len(add_stats_array) == 4:
                self.set_stats(name, add_stats_array)
                self.characters.update({'name': name}, {"$set": {'free_stats': current_stats - cost}})
                return "You have spent " + str(cost) + " stats. You have " + str(current_stats - cost) + " remaining."
        except:
            self.sys_log.error("Error allocating stats: " + str(sys.exc_info()))

    def equip_items(self, name, item_name, item_type, item_stats):
        try:
            if self.inventory.find({'name':name})[0][item_type] is not None:
                old_stats = self.inventory.find({'name':name})[0][item_type][1]
                neg_stats = [-1*i for i in old_stats]
                self.set_stats(name, neg_stats)
            self.inventory.update({'name': name}, {"$set": {item_type: [item_name, item_stats]}})
            self.set_stats(name, item_stats)
        except:
            self.sys_log.error("Error equipping items: " + str(sys.exc_info()))

    def export_to_web(self, local=True):
        if not local:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.scp_host, port=self.scp_port, key_filename=self.ssh_key, username=self.scp_user)
            sftp = ssh.open_sftp()
            for f in os.listdir(self.char_sheet_folder):
                sftp.put(self.char_sheet_folder + "/" + f, self.sftp_dir + "/" + f)
        else:
            for f in os.listdir(self.char_sheet_folder):
                shutil.copy(self.char_sheet_folder + "/" + f, self.sftp_dir)

    def fill_enemy_db(self, count):
        self.enemies.remove()
        for x in range(0, count):
            self.gen_creature(count)

    def gen_creature(self, difficulty):
        try:
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
            #self.sys_log.debug("Creature generated: " + str(char_post))
        except:
            self.sys_log.error("Error generating creature: " + str(sys.exc_info()))

    def gen_item(self):
        print

    def generate_character(self, char_name, in_str, in_vit, in_agi, in_dex):
        s_str = int(in_str)
        s_vit = int(in_vit)
        s_dex = int(in_dex)
        s_agi = int(in_agi)

        try:
            if (s_str + s_vit + s_dex + s_agi == self.max_start_stats) and (self.characters.find({"name": char_name}).count() == 0):
                (s_str, s_vit, s_dex, s_agi) = (s_str+1, s_vit+1, s_dex+1, s_agi+1)
                hp = s_vit * 5
                char_post = {"name": char_name, "level": 1, "xp": 0, "next_level": 100, "free_stats": 0, "hp": hp, "str": s_str, "vit": s_vit, "agi": s_agi, "dex": s_dex, "gold": 0}
                inven_post = {"name": char_name, "helm": None, "chest": None, "weapon": None, "legs": None, "boots": None, "items": []}
                self.inventory.insert(inven_post)
                self.characters.insert(char_post)
                self.sys_log.debug("Character created successfully: " + str(char_post))
            else:
                if self.characters.find({"name":char_name}).count() > 0:
                    return "Character already exists."
                if not (s_str + s_vit == self.max_start_stats):
                    return "Stats do not add up to " + str(self.max_start_stats) + "."

        except:
            self.sys_log.error("Error generating character: " + str(sys.exc_info()))

    def get_character_sheet(self, name):
        s_hp, s_str, s_vit, s_agi, s_dex = self.get_stats('riotgradius', self.characters)
        s_inven = self.inventory.find({'name': name})[0]
        cstring = ""
        cstring += "Character Name: " + name + '\n'
        cstring += "Level: " + str(self.characters.find({'name': name})[0]['level']) + "    XP: " + str(self.characters.find({'name': name})[0]['xp'])
        cstring += "    Next level: " + str(self.characters.find({'name': name})[0]['next_level']) + ' XP\n'
        cstring += "Gold: " + str(self.characters.find({'name': name})[0]['gold']) + '\n\n'
        cstring += "HP: " + str(s_hp) + "\n"
        cstring += "STR: " + str(s_str) + "\nVIT: " + str(s_vit) + "\nAGI: " + str(s_agi) + "\nDEX: " + str(s_dex) + "\n\n"
        cstring += "Equipment:\n"
        cstring += "Helm: " + str(s_inven['helm']) + '\n'
        cstring += "Chest: " + str(s_inven['chest']) + '\n'
        cstring += "Legs: " + str(s_inven['legs']) + '\n'
        cstring += "Boots: " + str(s_inven['boots']) + '\n\n'
        cstring += "Inventory: " + str(s_inven['items'])
        c_sheet_file = open(self.char_sheet_folder + "/" + name + "_sheet.txt", 'w')
        c_sheet_file.write(cstring)
        c_sheet_file.close()
        return cstring

    def get_stats(self, name, db):
        try:
            hp1, str1, vit1 = db.find_one({"name": name})["hp"], db.find_one({"name": name})["str"], db.find_one({"name": name})["vit"]
            agi1, dex1 = db.find_one({"name": name})["agi"], db.find_one({"name": name})["dex"]
            return hp1, str1, vit1, agi1, dex1
        except:
            self.sys_log.error("Error getting stats: ", sys.exc_info())

    def give_gold(self, name, gold):
        try:
            self.characters.update({'name': name}, {"$set": {'gold': self.characters.find({'name': name})[0]['gold'] + int(gold)}})
            self.sys_log.info("Gave " + name + " " + str(gold) + " gold.")
        except:
            self.sys_log.error("Error giving gold: ", sys.exc_info())

    def give_xp(self, name, xp):
        try:
            curr_xp = self.characters.find({'name': name})[0]['xp']
            curr_level = self.characters.find({'name': name})[0]['level']
            next_level = self.characters.find({'name': name})[0]['next_level']
            current_stats = self.characters.find({'name': name})[0]['free_stats']
            self.characters.update({'name': name}, {"$set": {'xp': curr_xp + int(xp) * self.xp_mod}})
            if curr_xp >= next_level:
                self.characters.update({'name': name}, {"$set": {'level': curr_level + 1}})
                self.characters.update({'name': name}, {"$set": {'xp': next_level - curr_xp}})
                self.characters.update({'name': name}, {"$set": {'next_level': next_level + next_level * self.xp_curve}})
                self.characters.update({'name': name}, {"$set": {'free_stats': current_stats + 5}})
        except:
            self.sys_log.error("Error giving xp : " + str(sys.exc_info()))

    def run_adventure(self, turns):
        try:
            ind = random.randint(0, self.enemies.count())
            enemy = self.enemies.find()[ind]['name']
            ind = random.randint(0, self.enemies.count())
            enemy2 = self.enemies.find()[ind]['name']
            self.run_combat(enemy, 'e', enemy2, 'e')
        except:
            print "Error running adventure: ", sys.exc_info()

    def run_combat(self, name1, type1, name2, type2):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        if type1 == 'e':
            db1 = self.enemies
            char1_log = logging.getLogger(name1)
            char1_ch = logging.StreamHandler(sys.stdout)
            char1_ch.setFormatter(formatter)
            char1_log.addHandler(char1_ch)
            char1_log.setLevel(logging.DEBUG)
        else:
            char1_log = logging.getLogger(name1 + '-combat-log')
            char1_log_hndl = logging.FileHandler('logs/chars/' + name1 + '_combat.log')
            char1_log_hndl.setFormatter(formatter)
            char1_log.addHandler(char1_log_hndl)
            char1_log.setLevel(logging.DEBUG)
            db1 = self.characters
        if type2 == 'e':
            db2 = self.enemies
            char2_log = logging.getLogger(name2)
            char2_ch = logging.StreamHandler(sys.stdout)
            char2_ch.setFormatter(formatter)
            char2_log.addHandler(char2_ch)
            char2_log.setLevel(logging.DEBUG)
        else:
            char2_log = logging.getLogger(name2 + '-combat-log')
            char2_log_hndl = logging.FileHandler('logs/chars/' + name2 + '_combat.log')
            char2_log_hndl.setFormatter(formatter)
            char2_log.addHandler(char2_log_hndl)
            char2_log.setLevel(logging.DEBUG)
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
                        char1_log.info(name1 + " hit " + name2 + " with " + str(str1) + " damage!")
                        char2_log.info(name1 + " hit " + name2 + " with " + str(str1) + " damage!")
                        hp2 -= str1
                    else:
                        char1_log.info(name1 + " missed " + name2 + "!")
                        char2_log.info(name1 + " missed " + name2 + "!")
                    turn = 2
                elif turn == 2:
                    hit_chance2 = (dex2 * self.hit_mod) / agi1
                    if random.random() < hit_chance2:
                        char1_log.info(name2 + " hit " + name1 + " with " + str(str2) + " damage!")
                        char2_log.info(name2 + " hit " + name1 + " with " + str(str2) + " damage!")
                        hp1 -= str2
                    else:
                        char1_log.info(name2 + " missed " + name1 + "!")
                        char2_log.info(name2 + " missed " + name1 + "!")
                    turn = 1
            if hp1 > hp2:
                char1_log.info(name1 + " has beaten " + name2 + " in combat!")
                char2_log.info(name1 + " has beaten " + name2 + " in combat!")
                char1_log.info('\n')
                char2_log.info('\n')
                return name1
            else:
                char1_log.info(name2 + " has beaten " + name1 + " in combat!")
                char2_log.info(name2 + " has beaten " + name1 + " in combat!")
                char1_log.info('\n')
                char2_log.info('\n')
                return name2

        except:
            self.sys_log.error("Error running combat: " + str(sys.exc_info()))

    def set_stats(self, name, stats_array):
        c_hp, c_str, c_vit, c_agi, c_dex = self.get_stats(name, self.characters)
        hp = c_vit * 5
        self.characters.update({'name': name}, {"$set": {'hp': hp}})
        self.characters.update({'name': name}, {"$set": {'str': c_str + stats_array[0]}})
        self.characters.update({'name': name}, {"$set": {'vit': c_vit + stats_array[1]}})
        self.characters.update({'name': name}, {"$set": {'agi': c_agi + stats_array[2]}})
        self.characters.update({'name': name}, {"$set": {'dex': c_dex + stats_array[3]}})