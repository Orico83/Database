"""
Author: Ori Cohen.
Date: 23/12/2022.
Tests the database in threads mode.
"""
from sync_db import SyncDb
from file_db import FileDb
import threading
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'
ENTER = "--------------------------------------------------\n"


def test_write(db):
    """
    Tests writing values to database
    :param db: database
    :return: None
    """
    logging.info("Write test started")
    for i in range(1000):
        assert db.set_value(i, f"t{str(i)}")
    logging.info("Write test successful")


def test_read(db):
    """
    Tests reading values from database
    :param db: database
    :return: None
    """
    logging.info("Read test started")
    for i in range(1000):
        assert db.get_value(i) == f"t{str(i)}"
    logging.info("Read test successful")


def test_delete(db):
    """
    Tests deleting values from database
    :param db: database
    :return: None
    """
    logging.info("Delete test started")
    for i in range(100):
        db.delete_value(i)
    for i in range(100):
        assert db.get_value(i) is None
    for i in range(100, 1000):
        assert db.get_value(i) == f"t{str(i)}"
    logging.info("delete test successful")


def main():
    logging.basicConfig(filename="ThreadTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    logging.info("Multithreading tests started")
    logging.info(ENTER)
    db = SyncDb(FileDb(), True)
    logging.info("Testing simple writing permissions")
    write = threading.Thread(target=test_write, args=(db,))
    write.start()
    write.join()
    logging.info(ENTER)
    logging.info("Testing simple reading permissions")
    read = threading.Thread(target=test_read, args=(db,))
    read.start()
    read.join()
    logging.info(ENTER)
    logging.info("Testing reading blocks writing")
    readers = []
    writers = []
    deletes = []
    for i in range(50):
        r = threading.Thread(target=test_read, args=(db,))
        readers.append(r)
    for i in range(5):
        w = threading.Thread(target=test_write, args=(db,))
        d = threading.Thread(target=test_delete, args=(db,))
        deletes.append(d)
        writers.append(w)
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.start()
    for delete in deletes:
        delete.start()
    for reader in readers:
        reader.join()
    for writer in writers:
        writer.join()
    for delete in deletes:
        delete.join()
    logging.info("Reading blocks writing test successful")
    logging.info(ENTER)
    logging.info("Testing writing blocks reading")
    readers = []
    writers = []
    for i in range(10):
        w = threading.Thread(target=test_write, args=(db,))
        writers.append(w)
    for i in range(50):
        r = threading.Thread(target=test_read, args=(db,))
        readers.append(r)
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.join()
    for reader in readers:
        reader.join()
    logging.info("Writing blocks reading test successful")
    logging.info(ENTER)


if __name__ == '__main__':
    main()
