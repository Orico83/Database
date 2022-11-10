class Db:
    def __init__(self):
        self.dictionary = dict()

    def set_value(self, key, val):
        self.dictionary[key] = val

    def get_value(self, key):
        try:
            return self.dictionary[key]
        except KeyError:
            return None

    def delete_value(self, key):
        val = self.dictionary[key]
        self.dictionary[key] = None
        return val


def main():
    database = Db()
    database.set_value('1', 'Hi')
    print(database.get_value('1'))
    x = database.get_value('0')
    print(x)
    val = database.delete_value('1')
    print(val)
    print(database.get_value('1'))


if __name__ == '__main__':
    main()
