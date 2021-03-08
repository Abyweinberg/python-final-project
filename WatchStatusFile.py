#!/usr/bin/env python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
from StatusFileHandler import *


class WatchStatusFile(FileSystemEventHandler):

    def __init__(self, station_id, file_name, client_connection, status_file_handler):
        self.patterns = str(file_name)
        self.ignore_patterns = ""
        self.ignore_directories = True
        self.case_sensitive = True
        self.event_handler = PatternMatchingEventHandler(
            self.patterns, self.ignore_patterns, self.ignore_directories, self.case_sensitive)
        self.status_file_handler = status_file_handler
        self.client_connection = client_connection

    def on_modified(self, event):
        if event.src_path == f'./{self.patterns}':
            print(f'The file {event.src_path} was {event.event_type}')
            valid_alarm_config = self.status_file_handler.check_file_validation()
            if valid_alarm_config:
                currently_alarm_status_from_file = self.client_connection.get_alarm_status_from_file()
                if currently_alarm_status_from_file != self.client_connection.alarm_status:
                    self.client_connection.update_alarm_status()
                    self.client_connection.update_server()

    # TODO on_delete
