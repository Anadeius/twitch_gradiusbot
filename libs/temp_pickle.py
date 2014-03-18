import pickle
import os


#wrapper for pickle to create temp files that are used to load and save dictionaries
class TempPickle():

    def __init__(self):
        return

    def load(self, file_name):
        if os.path.isfile(file_name):
            return_dict = pickle.load(open(file_name, "rb"))
        else:
            return_dict = {}

        return return_dict

    def save(self, dict_obj, file_name):
        pickle.dump(dict_obj, open(file_name, "wb"))