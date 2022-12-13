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
        """

        :return:
        """
        self.read.acquire()
        logging.info("SyncDb: Reading permission acquired")

    def read_release(self):
        """

        :return:
        """
        logging.info("SyncDb: Reading permission released")
        self.read.release()

    def write_get(self):
        """

        :return:
        """
        self.write.acquire()
        for i in range(10):
            self.read.acquire()
        logging.info("SyncDb: Writing permission acquired")

    def write_release(self):
        """

        :return:
        """
        logging.info("SyncDb: Writing permission released")
        for i in range(10):
            self.read.release()
        self.write.release()

    def get_value(self, key):
        """

        :param key:
        :return:
        """
        self.read_get()
        res = self.database.get_value(key)
        self.read_release()
        return res

    def set_value(self, key, val):
        """

        :param key:
        :param val:
        :return:
        """
        self.write_get()
        res = self.database.set_value(key, val)
        self.write_release()
        return res

    def delete_value(self, key):
        """

        :param key:
        :return:
        """
        self.write_get()
        self.database.delete_value(key)
        self.write_release()

