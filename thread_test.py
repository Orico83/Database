from sync_db import SyncDb
from file_db import FileDb
import threading
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'
ENTER = "\n--------------------------------------------------\n"


def test_write(db):
    logging.info("Write test started")
    for i in range(10000):
        assert db.set_value(i, f"t{str(i)}")


def test_read(db):
    logging.info("Read test started")
    for i in range(10000):
        assert db.get_value(i) == f"t{str(i)}"


def test_delete(db):
    logging.info("Delete test started")



def main():
    logging.basicConfig(filename="ThreadTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    logging.info("Multithreading tests started")
    logging.info(ENTER)
    db = SyncDb(FileDb(), True)
    logging.info("Testing simple writing permissions")
    t1 = threading.Thread(target=test_write, args=(db,))
    t1.start()
    t1.join()
    logging.info("Writing test successful")
    logging.info(ENTER)
    logging.info("Testing simple reading permissions")
    t1 = threading.Thread(target=test_read, args=(db,))
    t1.start()
    t1.join()
    logging.info("Reading test successful")
    logging.info(ENTER)


if __name__ == '__main__':
    main()
