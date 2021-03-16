#!/usr/bin/env python3

from os import path
import ast

# This class attempt to handle Static file modification and recover
class StatusFileHandler:

    def __init__(self, station_id, client_connection) -> None:
        self.station_id = station_id
        self.file_name = 'status' + station_id + '.txt'
        self.client_connection = client_connection

    def create_file(self, recover=False):
        if recover:
            get_data_from_db = input(
                'Do you want to recover the status file? y or n : ')
            if (get_data_from_db.lower() == 'y'):
                db_result = self.client_connection.get_alarm_status_from_db(
                    self.station_id)
                print(db_result)
                if db_result:
                    try:
                        data = ast.literal_eval(db_result)
                        with open(self.file_name, 'w') as f:
                            f.write(f'{self.station_id} {data[2]} {data[3]}')
                    except (ValueError, AttributeError, SyntaxError) as err:
                        pass
                else:
                    print("Something was wrong with the DB, I'll create a default file")
                    with open(self.file_name, 'w') as f:
                        f.write(f'{self.station_id} 0 0')
            else:
                print("Ok, Default file will be create")
                with open(self.file_name, 'w') as f:
                    f.write(f'{self.station_id} 0 0')
        elif path.isfile(self.file_name):
            print(
                'Status File detected, if any alarm is not decleared the default is False!')
        else:
            print("We detect status file doesn't exist, I will create it for you :-)")
            with open(self.file_name, 'w') as f:
                f.write(f'{self.station_id} 0 0')

    def check_file_validation(self):
        with open(self.file_name, 'r') as f:
            file_content = f.read()
            file_content = file_content.split()
            if len(file_content) == 3:
                if file_content[0] == self.station_id:
                    for index in range(1, 3):
                        try:
                            alarm = int(file_content[index])
                            if alarm < 0 or alarm > 1:
                                print('The Alarm should be 1 or 0')
                                return False
                        except ValueError:
                            print(ValueError)
                            print(f'''Error, the value in the column numnber: {index + 1} 
                            is not Integer, your input is {file_content[index]}''')
                else:
                    print('The File ID is not the same with client')
                    return False
            else:
                print('Error, The file should have only 3 columns')
                return False
            return True, file_content
