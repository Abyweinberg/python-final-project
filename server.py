#!/usr/bin/env python3

from client import Client
import sqlite3
import socket
from sqlite3.dbapi2 import Cursor
import datetime
import ast
import select
#test

class Server:

    def __init__(self, host, port):
        # Init SQL
        try:
            self.conn = sqlite3.connect("data.sqlite")
        except Exception as e:
            print(f'Exception connection to the DB: {e}')
        cur = self.conn.cursor()
        cmd = """
        CREATE TABLE IF NOT EXISTS station_status (
        station_id INT,last_date TEXT,alarm1 INT,alarm2 INT,PRIMARY KEY(station_id));"""
        cur.execute(cmd)
        self.conn.commit()

        # Init Socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((host, port))
            self.socket.listen(10)
        except Exception as e:
            print(f'Exception creating socket: {e}')
        print(f'[Server] - Initializaded and listen on {host}:{port}')

    def __del__(self):
        print('[Server] - Closing sql')
        self.conn.close()  # Close sql
        self.socket.close()  # Close Soket

        # Accept connection from Clients 
    def accept_connection(self): 
        (client_socket, client_addr) = self.socket.accept()
        print(
            f'[Server] - Accepted Connection: {client_addr}')
        return client_socket, client_addr

    def update_db(self, id, alarm1, alarm2):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
        parameter = (id, date, alarm1, alarm2)
        print(
            f'[Server] - Updating Client id Number {id} at Time: {date} - Alarm1: {alarm1} - Alarm2: {alarm2} ')
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "insert or replace into station_status (station_id,last_date, alarm1, alarm2) values (?,?, ?, ?)",
                parameter)
            self.conn.commit()
            print('DB updated')
        except Exception as e:
            print(f'Exception: {e}')

    def get_db_status(self, id):
        parameters = (str(id), )
        try:
            cur = self.conn.cursor()
            cur.execute(
                "select * from station_status where station_id = ?", parameters)
            result = cur.fetchone()
            print(f'[Server] - Retriving alarm status to the Client id {id}')
            print(f'Result: {result}')
            return result
        except Exception as e:
            print(f'Exception: {e}')
        
        # This Function procces the request of the client, 
        # Update to change alarms status and retrieve for recover in the case
        # the status file was removed.
    def process_data_client(self, data):
        data = data.decode()
        try:
            data = ast.literal_eval(data)
            if data['command'] == 'update':
                data = data['data'].split()
                self.update_db(data[0], data[1], data[2])
            elif data['command'] == 'retrieve':
                data = data['data'].split()
                return self.get_db_status(data[0])
            else:
                print('command not fount')
                return False
        except (ValueError, AttributeError, SyntaxError) as err:
            print(data)


if __name__ == '__main__':
    try:
        my_server = Server('localhost', 12121)
        client_list = []
        inputs_sockets = [my_server.socket]

        while inputs_sockets:
            readable, _, _ = select.select(inputs_sockets, [], [])

            for socket_readable in readable:
                if socket_readable is my_server.socket:
                    connection, client_address = my_server.socket.accept()
                    inputs_sockets.append(connection)
                else:
                    try:
                        data = socket_readable.recv(1024)
                        if data:
                            print(
                                f'Information from {socket_readable} = {data.decode()}')
                            result = my_server.process_data_client(data)
                            socket_readable.send(str(result).encode())

                    except ConnectionError as e:
                        pass

    except KeyboardInterrupt:
        print('The Server is shutting down')
        my_server.__del__()
