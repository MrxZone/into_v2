import random
import string

def get_random_nickname():
    return "".join(random.sample(string.ascii_letters, 6)) + "@Into"
