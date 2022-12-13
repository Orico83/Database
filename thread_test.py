from sync_db import SyncDb
from file_db import FileDb
import threading
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'
ENTER = "--------------------------------------------------\n"


def test_write(db):
    logging.info("Write test started")
    for i in range(100):
        assert db.set_value(i, f"t{str(i)}")
    logging.info("Writing test successful")


def test_read(db):
    logging.info("Read test started")
    for i in range(100):
        assert db.get_value(i) == f"t{str(i)}"
    logging.info("Reading test successful")


def test_delete(db):
    logging.info("Delete test started")
    for i in range(100):
        db.delete_value(i)
    for i in range(100):
        assert db.get_value(i) is None
    for i in range(100, 1000):
        assert db.get_value(i) == f"t{str(i)}"
    logging.info("deleting test successful")


def main():
    logging.basicConfig(filename="ThreadTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    logging.info("Multithreading tests started")
    logging.info(ENTER)
    db = SyncDb(FileDb(), True)
    logging.info("Testing simple writing permissions")
    t1 = threading.Thread(target=test_write, args=(db,))
    t1.start()
    t1.join()
    logging.info(ENTER)
    logging.info("Testing simple reading permissions")
    t1 = threading.Thread(target=test_read, args=(db,))
    t1.start()
    t1.join()
    logging.info(ENTER)
    """logging.info("Testing simple deleting permissions")
    t1 = threading.Thread(target=test_delete, args=(db,))
    t1.start()
    t1.join()
    logging.info(ENTER)"""
    logging.info("Testing reading blocks writing")
    readers = []
    writers = []
    for i in range(50):
        r = threading.Thread(target=test_read, args=(db,))
        readers.append(r)
    for i in range(10):
        w = threading.Thread(target=test_write, args=(db,))
        writers.append(w)
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.join()
    for writer in writers:
        writer.join()
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
