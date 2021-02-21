#!/usr/bin/env python3

from server import Server
from client import Client
# import client

myserver = Server('localhost', 33332)
print('Server waiting for a connection ... ')

my_client = Client(111, 'localhost', 33332)
# my_client2 = Client(222, 'localhost', 33332)
# my_client3 = Client(333, 'localhost', 33332)

client_conn, client_addr = myserver.accept_connection()

print(
    f'Connected by {client_addr} and this is the client connection: {client_conn}')


# while True:
# client_options = 'Test'

# client_conn.send(
#     f'Thanks for connecting your options are {client_options}'.encode())

# while True:
#     command = input('Please give your command: ')
#     if command == 'q' or command == 'Q':
#         print('Good Bye')
#         break
#     else:
#         print(f'The Server Response: {server_response}')
