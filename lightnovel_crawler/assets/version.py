import os

cur_dir = os.path.dirname(__file__)
ver_file = os.path.join(cur_dir, '..', '..', 'VERSION')
with open(ver_file, 'r') as f:
    version = f.read().strip()


def get_value():
    return version
