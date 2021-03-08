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
#  OLD CODE FROM SERVER.PY
        # try:
            #     thread = _thread.start_new_thread(my_server.create_new_connection_thread, (conn, addr))
            #     print(f'The thread is {thread}')
            # except Exception as e:
            #     print(f'The exception is : {e}')
        # conn, addr = threading.Thread(my_server.accept_connection())

        # with conn:
        #     # print(f'Connected with {addr}')
        #     while True:
        #         data = conn.recv(1024)
        #         print(f'Recived data: {data}')
        #         if not data:
        #             break
        #         conn.sendall(data)

    # def create_new_connection_thread(self, conn, addr):
    #     print(
    #         f'connected by {conn} and addr: {addr} from def create new connection thread')
    #     with conn:
    #         # print(f'Connected with {addr}')
    #         while True:
    #             data = conn.recv(1024)
    #             print(f'Recived data: {data}')
    #             if not data:
    #                 break
    #             conn.sendall(data)

    # def send_order_to_db(self, querry):
    #     try:
    #         cur = self.conn.cursor()
    #         cur.execute(querry)
    #         self.conn.commit()
    #     except Exception as e:
    #         print(f'Exception: {e}')

# OLD code from client.py
#    # def create_event_handler(self):
    #     patterns = '*'
    #     ignore_patterns = ""
    #     ignore_directories = True
    #     case_sensitive = True
    #     event_handler = PatternMatchingEventHandler(
    #         patterns, ignore_patterns, ignore_directories, case_sensitive)
    #     return event_handler

    # def on_deleted(self, event):
    #     print(f"hey, {event.src_path} has been DELETED!")

    # def on_modified(self, event):
    #     print(f"hey buddy, {event.src_path} has been modified")
    #     print(f'event type: {event.event_type}')
    #     print(f'Event: {event}')


   # EVENT HANDLER
    # my_event_handler = my_client.create_event_handler()
    # print(f'This is my event handler: {my_event_handler}')
    # # my_event_handler.on_created = my_client.on_created
    # my_event_handler.on_modified = my_client.on_modified
    # go_recursively = False
    # path_file = '/usr/local/projects/rt-ed/final_projects/python/'
    # my_observer = Observer()
    # print(f'This is my observ: {my_observer}')
    # my_observer.schedule(my_event_handler, path_file, recursive=go_recursively)
    # my_observer.start()
    # try:
    #     while True:
    #         print('Before sleep 10')
    #         time.sleep(10)
    #         print('After sleep 10')
    # except KeyboardInterrupt:
    #     my_observer.stop()
    #     my_observer.join()

    # if my_client.socket.recv(1024):
    # print(my_client.socket.recv(1024))

    # my_client = Client('2', 'localhost', 12121, file_name)
    # Check file status
    # my_client.update_alarm_status()
    # my_client.update_server()
    # ------------------------------------- Finish initialization -------------------------------------
    # print(f'status from my_client: {my_client.file_status}')
    # new_list = ['2', '0', '0']
    # if my_client.file_status == new_list:
    #     print('idem')
    # else:
    #     print('not idem')