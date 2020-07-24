import os
import tempfile
from random import choice
from string import ascii_uppercase


class File:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        with open(path_to_file, 'a') as f:
            pass

    def read(self):
        with open(self.path_to_file, 'r') as f:
            s = f.read()
        return s

    def write(self, string):
        with open(self.path_to_file, 'w') as f:
            f.write(string)
        return len(string)

    def __add__(self, other):
        s = ''.join(choice(ascii_uppercase) for i in range(12))
        a = File(os.path.join(tempfile.gettempdir(), s))
        with open(a.path_to_file, 'w') as f:
            f.write(self.read())
        with open(a.path_to_file, 'a') as f:
            f.write(other.read())
        return a

    def __str__(self):
        return os.path.abspath(self.path_to_file)

    def __getitem__(self, item):
        with open(self.path_to_file) as f:
            s = f.readlines()
        return s[item]
