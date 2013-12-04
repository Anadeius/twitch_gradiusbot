import thread


class MessageProcessor():

    def __init__(self):
        print "Message processor initialized."

    def thread_message(self, message_function, arg_tuple):
        thread.start_new_thread(message_function, arg_tuple)