import random
import string


def random_str(length=10):
    all_str = string.digits + string.ascii_lowercase
    return ''.join(random.sample(all_str, length))
