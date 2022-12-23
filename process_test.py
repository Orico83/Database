"""
Author: Ori Cohen
Date: 23/12/2022
Tests the database in processes mode.
"""


from sync_db import SyncDb
from file_db import FileDb
import multiprocessing
from thread_test import test_read, test_write, test_delete


ENTER = "--------------------------------------------------\n"


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
    print("Testing reading blocks writing")
    readers = []
    writers = []
    deletes = []
    for i in range(50):
        r = multiprocessing.Process(target=test_read, args=(db,))
        readers.append(r)
    for i in range(10):
        w = multiprocessing.Process(target=test_write, args=(db,))
        d = multiprocessing.Process(target=test_delete, args=(db,))
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
    print("Reading blocks writing test successful")
    print(ENTER)
    print("Testing writing blocks reading")
    readers = []
    writers = []
    write = multiprocessing.Process(target=test_write, args=(db,))
    write.start()
    write.join()
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


if __name__ == '__main__':
    main()
