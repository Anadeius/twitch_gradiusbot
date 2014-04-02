import time
from libs.temp_pickle import TempPickle


class Throttling():

    def __init__(self):
        self.last_used_file = 'libs/tmp/last_used.tmp'
        self.rate_limit_file = 'libs/tmp/rate_limit.tmp'
        self.tmp_file = TempPickle()
        self.last_used = self.tmp_file.load(self.last_used_file)
        self.rate_limits = self.tmp_file.load(self.rate_limit_file)

    #Rate limiting on a command basis
    #Prevents spamming of single commands without stopping functionality of other commands
    def can_use_command(self, user, command):

        self.last_used = self.tmp_file.load(self.last_used_file)

        if (user, command) not in self.last_used.keys():
            self.last_used[(user, command)] = [time.time(), 1]
            self.tmp_file.save(self.last_used, self.last_used_file)
            return True

        else:
            use_count = self.last_used[(user, command)][1]

            #Check for rate limit reset time
            if time.time() - self.last_used[user, command][0] > self.rate_limits[command][1]:
                self.last_used[(user, command)] = [time.time(), 1]
                self.tmp_file.save(self.last_used, self.last_used_file)
                return True

            #Check for how many uses and if this violates rate limit
            elif use_count >= self.rate_limits[command][0]:
                return False

            else:
                count = self.last_used[(user, command)][1] + 1
                self.last_used[(user, command)] = [time.time(), count]
                self.tmp_file.save(self.last_used, self.last_used_file)
                return True

    #Set each command's rate limit individually
    def set_rate_limit(self, command, uses, reset_seconds):
        self.rate_limits = self.tmp_file.load(self.rate_limit_file)
        self.rate_limits[command] = [uses, reset_seconds]
        self.tmp_file.save(self.rate_limits, self.rate_limit_file)
