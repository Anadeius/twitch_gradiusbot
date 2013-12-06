import pymongo


class ChatRpg():

    def __init__(self):
        client = pymongo.MongoClient()
        rpg_db = client.trivia_db
        self.characters = rpg_db.characters
        self.inventory = rpg_db.inventory

    def generate_character(self):
        print

    def save_character(self):
        print

    def export_character_sheet(self):
        print