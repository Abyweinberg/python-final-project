#!/usr/bin/env python3

from StatusFileHandler import StatusFileHandler
import socket
import time
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
        print('Inside client init constructor')
        # print(self.socket.recv(1024).decode())

    def __del__(self):
        self.socket.close()

    # TODO check the self with an object? how? this should be auto without provide obj
    def __eq__(self, o: object) -> bool:
        return (self.alarm_status == o.alarm_status)

    # first udpate_alarm_status client_connection.update_alarm_status()
    # Second client_connection.update_server()
    # Done this function send to the server the alarm status
    # TODO Server should reply !!
    def update_server(self):
        data = ' '.join(self.alarm_status)
        packet = {'data': data, 'command': 'update'}
        res = self.socket.send(str(packet).encode())
        response = self.socket.recv(1024).decode()
        print(f'this is response: {response}')
        print(f'this is res: {res.decode()}')
        return response

    # Done
    def get_alarm_status_from_file(self):
        with open(self.alarm_status_file_name, 'r') as f:
            alarm_status = f.read()
            alarm_status = alarm_status.split()
            return alarm_status  # this return something like ['2','0','0']

    def get_alarm_status_from_db(self):
        # msg = ''
        pass

    # Done this function update the alarm_status, inside the object
    def update_alarm_status(self):
        alarm_status = self.get_alarm_status_from_file()
        self.alarm_status = alarm_status
        print(f'Alarm status update to {alarm_status}')


if __name__ == '__main__':
    # GET USER INFORMATION
    # Initilize Station with id
    # station_id = input('Please, Add the Station ID: ')
    station_id = '1'
    # Create status file name with the Station ID
    file_name = 'status' + station_id + '.txt'

    # Get Server IP and Port
    # server_ip = input('Server ip: ')
    # port = int(input('Port: '))
    server_ip = 'localhost'
    port = 12121

    # CREATE CLIENT OBJECT
    client_connection = Client(station_id, server_ip, port, file_name)
    print(f'New Client Started {client_connection}')
    client_connection.socket.send(b'This was send from the client')
    client_connection.update_alarm_status()

    # CREATE FILE HANDLER
    status_file_handler = StatusFileHandler(station_id, client_connection)
    status_file_handler.create_file()  # if not exist create else do nothing

    # CREATE EVENT HANDLER
    event_handler = WatchStatusFile(
        station_id, file_name, client_connection, status_file_handler)
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=False)
    print('Monitorin Started')
    observer.start()

    try:
        while True:
            time.sleep(1)
            recv = client_connection.socket.recv(1024)
            if recv:
                print(f'This msg comes from the server: {recv}')
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
