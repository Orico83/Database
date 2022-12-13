"""
Author: Ori Cohen.
Date: 13/12/2022.
"""


class Db:
    def __init__(self):
        """
        Database constructor.
        """
        self.database = {}

    def set_value(self, key, val):
        """
        Updates the value of the key or adds the key and the value to the database.
        :param key:
        :param val:
        :return:
        """
        self.database[key] = val
        return True

    def get_value(self, key):
        """

        :param key:
        :return: The value of the key. If the key isn't in the database, returns None.
        """
        try:
            return self.database[key]
        except KeyError:
            return None

    def delete_value(self, key):
        """

        :param key:
        :return:
        """
        try:
            return self.database.pop(key)
        except KeyError:
            return None
