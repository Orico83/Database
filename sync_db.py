"""
Author: Ori Cohen
Date: 23/12/2022
Implements the synchronization between threads/processes and reading and writing permissions.
"""


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

    def read_acquire(self):
        """
        Acquire reading permission
        :return: None
        """
        self.read.acquire()
        logging.info("SyncDb: Reading permission acquired")

    def read_release(self):
        """
        Release reading permissions
        :return: None
        """
        logging.info("SyncDb: Reading permission released")
        self.read.release()

    def write_acquire(self):
        """
        Acquire writing permission
        :return: None
        """
        self.write.acquire()
        for i in range(10):
            self.read.acquire()
        logging.info("SyncDb: Writing permission acquired")

    def write_release(self):
        """
        Release writing permission
        :return: None
        """
        logging.info("SyncDb: Writing permission released")
        for i in range(10):
            self.read.release()
        self.write.release()

    def get_value(self, key):
        """
        Acquire reading permission, get the key's value and then release writing permission.
        :param key: key
        :return: The key's value
        """
        self.read_acquire()
        res = self.database.get_value(key)
        self.read_release()
        return res

    def set_value(self, key, val):
        """
        Acquire writing permission, update the key's value and then release writing permission.
        :param key: key
        :param val: value to set
        :return: True if succeeded. Else, False.
        """
        self.write_acquire()
        res = self.database.set_value(key, val)
        self.write_release()
        return res

    def delete_value(self, key):
        """
        Acquire writing permission, delete the key's value and then release writing permission.
        :param key: key
        :return: The deleted value
        """
        self.write_acquire()
        val = self.database.delete_value(key)
        self.write_release()
        return val
