#!/usr/bin/env python3

import sqlite3
import socket
import _thread


class Server:

    def __init__(self, host, port):
        # Init SQL
        self.conn = sqlite3.connect("data.sqlite")
        cur = self.conn.cursor()
        cmd = """
        CREATE TABLE IF NOT EXISTS station_status (
        station_id INT,last_date TEXT,alarm1 INT,alarm2 INT,PRIMARY KEY(station_id));"""
        cur.execute(cmd)
        self.conn.commit()

        # Init Socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        print('Inside init Server')
        print(self.socket)

    def __del__(self):
        self.conn.close()  # Close sql
        self.socket.close()  # Close Soket

    def accept_connection(self):
        new_connection = self.socket.accept()
        print(f'Accepted Connection from: {new_connection}')
        return new_connection

    def update_db(id, alarm1, alarm2):
        pass
        # TODO Update db by id - must have the date


# TODO Create multiple connection using threads
if __name__ == '__main__':
    try:
        my_server = Server('localhost', 12121)
        # input('Waiting...')

        conn, addr = my_server.accept_connection()
        with conn:
            print(f'Connected with {addr}')
            while True:
                data = conn.recv(1024)
                print(f'Recived data: {data}')
                if not data:
                    break
                conn.sendall(data)
    except KeyboardInterrupt:
        pass
    finally:
        print('The Server is shutting down')
        my_server.__del__()
