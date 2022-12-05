from file_db import FileDb
import threading
import multiprocessing


class SyncDb:
    def __init__(self, db: FileDb, threaded):
        self.database = db
        if threaded:
            self.read = threading.Semaphore(10)
            self.write = threading.Lock()
        else:
            self.read = multiprocessing.Semaphore(10)
            self.write = multiprocessing.Lock()

    def read_get(self):
        self.read.acquire()

    def read_release(self):
        self.read.release()

    def write_get(self):
        self.write.acquire()
        for i in range(10):
            self.read.acquire()

    def write_release(self):
        for i in range(10):
            self.read.release()
        self.write.release()

    def get_value(self, key):
        self.read_get()
        res = self.database.get_value(key)
        self.read_release()
        return res

    def set_value(self, key, val):
        self.write_get()
        res = self.database.set_value(key, val)
        self.write_release()
        return res

    def delete_value(self, key):
        self.write_get()
        self.database.delete_value(key)
        self.write_release()


def main():
    pass


if __name__ == '__main__':
    main()
