from sync_db import SyncDb
from file_db import FileDb
import multiprocessing


ENTER = "--------------------------------------------------\n"


def test_write(db):
    print("Write test started")
    for i in range(1000):
        assert db.set_value(i, f"t{str(i)}")
    print("Writing test successful")


def test_read(db):
    print("Read test started")
    for i in range(1000):
        assert db.get_value(i) == f"t{str(i)}"
    print("Reading test successful")


def test_delete(db):
    print("Delete test started")
    for i in range(100):
        db.delete_value(i)
    for i in range(100):
        assert db.get_value(i) is None
    for i in range(100, 1000):
        assert db.get_value(i) == f"t{str(i)}"
    print("deleting test successful")


def main():
    print("Multithreading tests started")
    print(ENTER)
    db = SyncDb(FileDb(), False)
    print("Testing simple writing permissions")
    write = multiprocessing.Process(target=test_write, args=(db,))
    write.start()
    write.join()
    print(ENTER)
    print("Testing simple reading permissions")
    read = multiprocessing.Process(target=test_read, args=(db,))
    read.start()
    read.join()
    print(ENTER)
    """print("Testing simple deleting permissions")
    p1 = threading.Thread(target=test_delete, args=(db,))
    p1.start()
    p1.join()
    print(ENTER)"""
    print("Testing reading blocks writing")
    readers = []
    writers = []
    for i in range(50):
        r = multiprocessing.Process(target=test_read, args=(db,))
        readers.append(r)
    for i in range(10):
        w = multiprocessing.Process(target=test_write, args=(db,))
        writers.append(w)
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.join()
    for writer in writers:
        writer.join()
    print("Reading blocks writing test successful")
    print(ENTER)
    print("Testing writing blocks reading")
    readers = []
    writers = []
    for i in range(10):
        w = multiprocessing.Process(target=test_write, args=(db,))
        writers.append(w)
    for i in range(50):
        r = multiprocessing.Process(target=test_read, args=(db,))
        readers.append(r)
    for writer in writers:
        writer.start()
    for reader in readers:
        reader.start()
    for writer in writers:
        writer.join()
    for reader in readers:
        reader.join()
    print("Writing blocks reading test successful")
    print(ENTER)
    print("Testing delete permissions")
    delete = multiprocessing.Process(target=test_delete, args=(db,))
    delete.start()
    delete.join()


if __name__ == '__main__':
    main()
