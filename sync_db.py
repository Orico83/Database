from threading import *
from file_db import FileDb


class SyncDb:
    def __init__(self, db: FileDb, threading):
        self.db = db
        if threading:

        else:
            pass

    def read(self):
        self.db.load()
