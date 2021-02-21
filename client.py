#!/usr/bin/env python3

import socket
import sys
from os import path


class Client:

    alarm_status = []

    def __init__(self, id, host, port, alarm_status_file_name):
        self.id = id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.alarm_status_file_name = alarm_status_file_name
        print('Inside client init constructor')
        # print(self.socket.recv(1024).decode())

    def __del__(self):
        self.socket.close()

    def update_server(self):
        msg = ' '.join(self.alarm_status)
        self.socket.send(msg.encode())
        response = self.socket.recv(1024).decode()
        print(response)
        return response

    def __eq__(self, o: object) -> bool:
        return (self.alarm_status == o.alarm_status)

    def check_alarm_status(self):
        with open(self.alarm_status_file_name, 'r') as f:
            alarm_status = f.read()
            alarm_status = alarm_status.split()
            return alarm_status  # this return something like ['2','0','0']

    def update_alarm_status(self):
        alarm_status = self.check_alarm_status()
        self.alarm_status = alarm_status
        # TODO Should check the already information stored in a list


if __name__ == '__main__':
    # ------------------------------------- Start initialization -------------------------------------
    # Initilize Station with id
    station_id = input('Please, Add the Station ID: ')

    # Create status file name with the Station ID
    file_name = 'status' + station_id + '.txt'

    # Check if file exist else create itCreate
    if path.isfile(file_name):
        print(
            'Status File detected, if any alarm is not decleared the default is False!')
    else:
        print("We detect status file doesn't exist, I will create it for you :-) ")
        with open(file_name, 'w') as f:
            f.write(f'{station_id} 0 0')

    # Get Server IP and Port
    server_ip = input('Server ip: ')
    port = int(input('Port: '))

    # Create client object
    my_client = Client(station_id, server_ip, port, file_name)
    # my_client = Client('2', 'localhost', 12121, file_name)
    # Check file status
    my_client.update_alarm_status()
    my_client.update_server()

    # ------------------------------------- Finish initialization -------------------------------------

    # print(f'status from my_client: {my_client.file_status}')
    # new_list = ['2', '0', '0']
    # if my_client.file_status == new_list:
    #     print('idem')
    # else:
    #     print('not idem')

    input('Waiting....')
