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
        with open(FILE, 'rb') as file:
            self.database = pickle.load(file)

    def dump(self):
        with open(FILE, 'wb') as file:
            pickle.dump(self.database, file)

    def set_value(self, key, val):
        try:
            self.load()
            res = super().set_value(key, val)
            self.dump()
            return res
        except OSError as err:
            print(err)
            return False

    def get_value(self, key):
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        self.load()
        res = super().delete_value(key)
        self.dump()
        return res


def main():
    db = FileDb()
    check = db.set_value(4, 2)
    db.set_value(3, 5)
    print(check)
    print(db.get_value(4))
    db.delete_value(4)
    db.delete_value(5)
    print(db.get_value(4))


if __name__ == '__main__':
    main()