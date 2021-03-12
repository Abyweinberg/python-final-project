#!/usr/bin/env python3

import sqlite3
import socket
from sqlite3.dbapi2 import Cursor, threadsafety
import datetime
import ast

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
        print(f'Server Initializaded and listen on {host}:{port}')

    def __del__(self):
        self.conn.close()  # Close sql
        self.socket.close()  # Close Soket

    def accept_connection(self):
        (client_socket, client_addr) = self.socket.accept()
        print(
            f'Accepted Connection from addres: {client_addr}')
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

    def process_data_client(self, data):
        data = data.decode()
        try:
            data = ast.literal_eval(data)
            if data['command'] == 'update':
                data = data['data'].split()
                self.update_db(data[0], data[1], data[2])
        # TODO Have to check wich execption could be
        except (ValueError, AttributeError, SyntaxError) as err:
            print(f'Exception {err}')
            print(data)
            pass


if __name__ == '__main__':
    try:
        my_server = Server('localhost', 12121)
        # my_server.get_db_status(2)
        # my_server.update_db(613, 1, 1)
        # my_server.get_db_status(613)
        conn, addr = my_server.accept_connection()

        while True:
            data = conn.recv(1024)
            if data:
                # print(f'Information from {conn} = {data.decode()}')
                # my_server.socket.send()
                conn.send('Proccesing your request'.encode())
                my_server.proccess_data_client(data)

        # while True:
        #     recv = conn.recv(1024).decode()
        #     print(f'Server get this msg: {recv}')
        #     # TODO send response to Client
        #     if recv:
        #         conn.send(b'Server Send from server.py')

    except KeyboardInterrupt:
        print('The Server is shutting down')
        my_server.__del__()
