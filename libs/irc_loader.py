## Module loader written specifically for IRC
from neoLoader import NeoLoader


class IrcLoader():
    modList = {}
    nl = NeoLoader()

    def __init__(self):
        print "IRC loader started."

    ## Uses neoloader to load the modules
    def load(self, modPath, message_callback_function):
        split = modPath.split('/')
        name = split[len(split) - 1]
        self.modList[name] = self.nl.loadMod(modPath)
        self.modList[name].buildup(message_callback_function)

    def unload(self, name):
        self.modList[name].teardown()
        del self.modList[name]

    def listMods(self):
        ans = []
        for i, j in self.modList.iteritems():
            ans.append(i)
        return ans

    def run(self, module, inp, sender, channel):
        ## Sends the user input to the plugin
        self.modList[module].send_input(inp, sender, channel)

    def desc(self, module):
        ## Runs the desc method for the module
        return self.modList[module].desc()
