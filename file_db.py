import pickle
from db import Db
import os

FILE = "database.bin"


class FileDb(Db):
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

        :param key:
        :param val:
        :return:
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

        :param key:
        :return:
        """
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        """

        :param key:
        :return:
        """
        self.load()
        res = super().delete_value(key)
        self.dump()
        return res
