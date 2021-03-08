#!/usr/bin/env python3

import sqlite3
import socket
import _thread
from sqlite3.dbapi2 import Cursor, threadsafety
import threading
import datetime

# TODO Create date in db!


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
        print('Server Initializaded')

    def __del__(self):
        self.conn.close()  # Close sql
        self.socket.close()  # Close Soket

    def accept_connection(self):
        (client_socket, client_addr) = self.socket.accept()
        print(
            f'Accepted Connection from: {client_socket} with the addres: {client_addr}')
        return client_socket, client_addr

    def update_db(self, id, alarm1, alarm2):
        date = datetime.datetime.now().strftime('%Y-%M-%d %H:%m')
        querry = f'''insert or replace into station_status (station_id,
                    last_date, alarm1, alarm2) values ({id},'{date}', {alarm1}, {alarm2})'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(querry)
            self.conn.commit()
        except Exception as e:
            print(f'Exception: {e}')
        # TODO Update db by id - must have the date

    def get_db_status(self, id):
        # TODO secure id
        querry = f'''select * from station_status where station_id = {str(id)}'''
        # querry = f'''select * from station_status'''
        try:
            cur = self.conn.cursor()
            cur.execute(querry)
            # self.conn.commit()
            result = cur.fetchone()
        except Exception as e:
            print(f'Exception: {e}')

        print(result)
        return result


if __name__ == '__main__':
    try:
        my_server = Server('localhost', 12121)
        my_server.get_db_status(2)
        my_server.update_db(613, 1, 1)
        my_server.get_db_status(613)

        while True:
            conn, addr = my_server.accept_connection()
            recv = conn.recv(1024).decode()
            print(f'Server get: {recv}')
            # TODO send response to Client
            if recv:
                conn.send(b'Server Receive get msg')

    except KeyboardInterrupt:
        print('The Server is shutting down')
        my_server.__del__()
