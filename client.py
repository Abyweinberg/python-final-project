#!/usr/bin/env python3

from StatusFileHandler import StatusFileHandler
import socket
from watchdog.observers import Observer
from WatchStatusFile import *


class Client:

    alarm_status = []
    file_name = ''

    def __init__(self, id, host, port, alarm_status_file_name):
        self.id = id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.alarm_status_file_name = alarm_status_file_name
        print(f'[Client id {id}] - Initialized Client')

    def __del__(self):
        print(f'Client id [{self.id}] - Closing socket')
        self.socket.close()

    def update_server(self):
        data = ' '.join(self.alarm_status)
        packet = {'data': data, 'command': 'update'}
        try:
            self.socket.send(str(packet).encode())
            response = self.socket.recv(1024).decode()
            return response
        except Exception as e:
            print(f'Error updating Server: {e}')
            return False

    def get_alarm_status_from_file(self):
        with open(self.alarm_status_file_name, 'r') as f:
            alarm_status = f.read()
            alarm_status = alarm_status.split()
            return alarm_status  # this return something like ['2','0','0']

    def get_alarm_status_from_db(self, id):
        packet = {'data': f'{id}', 'command': 'retrieve'}
        try:
            self.socket.send(str(packet).encode())
            return self.socket.recv(1024).decode()
        except Exception as e:
            print(f'Error getting alarm status: {e}')
            return False

    def update_alarm_status(self):
        alarm_status = self.get_alarm_status_from_file()
        self.alarm_status = alarm_status
        print(f'Client id [{self.id}] - {alarm_status}')


if __name__ == '__main__':
    # GET USER INFORMATION
    # Initilize Station with id
    station_id = input('Please, Add the Station ID: ')
    # Create status file name with the Station ID
    file_name = 'status' + station_id + '.txt'

    # Get Server IP and Port
    server_ip = input('Server ip: ')
    port = int(input('Port: '))

    # CREATE CLIENT OBJECT
    client_connection = Client(station_id, server_ip, port, file_name)
    print(f'New Client id {station_id} Started {client_connection.socket}')

    # CREATE FILE HANDLER
    status_file_handler = StatusFileHandler(station_id, client_connection)
    status_file_handler.create_file()  # if not exist create else do nothing

    client_connection.update_alarm_status()
    client_connection.update_server()

    # CREATE EVENT HANDLER
    event_handler = WatchStatusFile(
        station_id, file_name, client_connection, status_file_handler)
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=False)
    print('WatchStatusFile Monitorin Started')
    observer.start()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
