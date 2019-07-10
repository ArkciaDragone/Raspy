'''
Test File
Please write your test code here
Note that this file could be modified by anyone
'''
from multiprocessing import Process, Pipe
from time import sleep


def f(conn):
    sleep(3)
    conn.send([42, None, 'hello'])
    conn.close()


class Runner():
    def __init__(self, conn):
        print("Runners on their way!")
        self.conn = conn
        sleep(2)
        conn.send("Got it!")
        self.z()

    def z(self):
        print("zing...")
        sleep(2)
        print("zed w")


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=Runner, args=(child_conn,))
    p.start()
    print(parent_conn.recv())  # prints "[42, None, 'hello']"
    p.join()
