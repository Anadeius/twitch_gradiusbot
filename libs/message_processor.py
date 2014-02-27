from multiprocessing import Process


class MessageProcessor():

    def __init__(self):
        print "Message processor initialized."

    def create_process(self, message_function, arg_tuple):
        p = Process(target=message_function, args=arg_tuple)
        p.start()