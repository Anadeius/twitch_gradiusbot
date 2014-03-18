import time


class Throttling():

    def __init__(self):
        self.last_used = {}
        self.rate_limits = {}

    #Rate limiting on a command basis
    #Prevents spamming of single commands without stopping functionality of other commands
    def can_use_command(self, user, command):
        now = time.time()

        if (user, command) not in self.last_used.keys():
            self.last_used[(user, command)] = [time.time(), 1]
            return True

        else:
            use_count = self.last_used[(user, command)][1]

            #Check for rate limit reset time
            if time.time() - self.last_used[user, command][0] > self.rate_limits[command][1]:
                self.last_used[(user, command)] = [time.time(), 1]
                return True

            #Check for how many uses and if this violates rate limit
            elif use_count >= self.rate_limits[command][0]:
                return False

            else:
                count = self.last_used[(user, command)][1] + 1
                self.last_used[(user, command)] = [time.time(), count]
                return True


    #Set each command's rate limit individually
    def set_rate_limit(self, command, uses, reset_seconds):
        self.rate_limits[command] = [uses, reset_seconds]