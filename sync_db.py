from file_db import FileDb
import threading
import multiprocessing
import logging


FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


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
        logging.info("SyncDb: Reading permission acquired")
        self.write.acquire()

    def read_release(self):
        self.read.release()
        logging.info("SyncDb: Reading permission released")

    def write_get(self):
        self.write.acquire()
        logging.info("SyncDb: Writing permission acquired")
        for i in range(10):
            logging.info(i)
            self.read.acquire()

    def write_release(self):
        for i in range(10):
            self.read.release()
        self.write.release()
        logging.info("SyncDb: Writing permission released")

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
