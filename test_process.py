from sync_db import SyncDb
from file_db import FileDb
import multiprocessing
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


def test_write(db):
    logging.debug("started write test")
    for i in range(1000):
        assert db.set_value(i, "test" + str(i))


def test_read(db):
    logging.debug("started read test")
    for i in range(1000):
        assert "test" + str(i) == db.get_value(i)


def main():
    logging.debug("Starting tests for Multiprocessing")
    db = SyncDb(FileDb(), False)
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple write perms")
    p1 = multiprocessing.Process(target=test_write, args=(db, ))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple read perms")
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing read blocks writing")
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p2 = multiprocessing.Process(target=test_write, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing write blocks reading")
    p1 = multiprocessing.Process(target=test_write, args=(db, ))
    p2 = multiprocessing.Process(target=test_read, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing multi reading perms possible")
    processes = []
    for i in range(5):
        process = multiprocessing.Process(target=test_read, args=(db, ))
        process.start()
        processes.append(process)
    for i in processes:
        i.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing load")
    processes = []
    for i in range(15):
        process = multiprocessing.Process(target=test_read, args=(db, ))
        process.start()
        processes.append(process)
    for i in range(5):
        p1 = multiprocessing.Process(target=test_write, args=(db,))
        p1.start()
        processes.append(p1)
    for i in processes:
        i.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing values stay correct")
    p1 = multiprocessing.Process(target=test_read, args=(db,))
    p1.start()
    p1.join()
    logging.info("test successful")


if __name__ == '__main__':
    logging.basicConfig(filename="ProcessTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    main()