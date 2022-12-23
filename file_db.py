"""
Author: Ori Cohen
Date: 23/12/2022
File database class with writing, reading and deleting capabilities to database.bin.
Inherits from DB.
"""


import pickle
from db import Db
import os

FILE = "database.bin"


class FileDb(Db):
    """
    File database constructor
    """
    def __init__(self):
        super().__init__()
        if not os.path.exists(FILE):
            with open(FILE, "wb") as file:
                pickle.dump({}, file)

    def load(self):
        """
        Loads the database from the file.
        :return: None.
        """
        with open(FILE, 'rb') as file:
            self.database = pickle.load(file)

    def dump(self):
        """
        Updates the database to the file.
        :return: None.
        """
        with open(FILE, 'wb') as file:
            pickle.dump(self.database, file)

    def set_value(self, key, val):
        """
        Updates the value of the key to the file if key is in the database.
        Else, adds the key and the value to the file database
        :param key: key
        :param val: value to set
        :return: True if succeeded. Else, False
        """
        try:
            self.load()
            res = super().set_value(key, val)
            self.dump()
            return res
        except OSError as err:
            print(err)
            return False

    def get_value(self, key):
        """
        Return the value of key if it's in database, else None
        :param key: key
        :return: The value of the key. If the key isn't in the database, returns None
        """
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        """
        Deletes the value of key in the file dict and returns it if it's in database. Else, None
        :param key: key
        :return: Deleted value if key exists. Else, None
        """
        self.load()
        res = super().delete_value(key)
        self.dump()
        return res
