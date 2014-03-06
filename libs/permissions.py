import pickle
import os

class Permissions():

    def __init__(self):
        print "Initializing permissions."
        self.file_name = "libs/permissions.tmp"

        if os.path.isfile(self.file_name):
            self.load()

        else:
            self.perms = {}

    def add_tag(self, nick, tag):
        self.load()

        if nick in self.perms.keys():
            if not tag in self.perms[nick]:
                self.perms[nick].append(tag)
        else:
            self.perms[nick] = [tag]

        self.save()

    def has_tag(self, nick, tag):
        self.load()

        if nick in self.perms.keys():
            return tag in self.perms[nick]

        else:
            return False

    def list_tags(self, nick):
        self.load()

        if nick in self.perms.keys():
            return self.perms[nick]

    def rem_tag(self, nick, tag):
        self.load()

        if nick in self.perms.keys():
            if tag in self.perms[nick]:
                self.perms[nick].remove(tag)

        self.save()


    def save(self):
        pickle.dump(self.perms, open(self.file_name, "wb"))

    def load(self):
        self.perms = pickle.load(open(self.file_name, "rb"))
