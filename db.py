class Db:
    def __init__(self):
        self.database = {}

    def set_value(self, key, val):
        self.database[key] = val
        return True

    def get_value(self, key):
        try:
            return self.database[key]
        except KeyError:
            return None

    def delete_value(self, key):
        try:
            val = self.database.pop(key)
            return val
        except KeyError as err:
            return None


def main():
    database = Db()
    database.set_value('1', 'Hi')
    print(database.get_value('1'))
    x = database.get_value('0')
    print(x)
    val = database.delete_value('1')
    print(val)
    print(database.get_value('1'))
    database.set_value('2', 'Hello')
    val = database.delete_value('2')
    print(val)
    print(database.get_value('2'))



if __name__ == '__main__':
    main()
