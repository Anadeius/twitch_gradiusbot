import libs.load_temp as temp

class Permissions():

    def __init__(self):
        print "Initializing permissions."
        self.t_file = "libs/permissions.tmp"
        self.data = temp.load_temp(self.t_file)

    def isOwner(self,nick):
        return self.data['owner'] == nick

    def isMod(self,nick):
        return nick in self.data['mods'].split(' ')

    def addMod(self,nick):
        temp_list = self.data['mods'].split()
        temp_list.append(nick)
        self.data['mods'] = ' '.join(temp_list)
        temp.save_temp(self.t_file, self.data)

    def remMod(self,nick):
        temp_list = self.data['mods'].split()
        temp_list.remove(nick)
        self.data['mods'] = ' '.join(temp_list)
        temp.save_temp(self.t_file, self.data)

    def listMods(self):
        return self.data['mods']
