#!/usr/bin/env python3

from os import path


class StatusFileHandler:

    def __init__(self, station_id) -> None:
        self.station_id = station_id
        self.file_name = 'status' + station_id + '.txt'

    def create_file(self):
        if path.isfile(self.file_name):
            print(
                'Status File detected, if any alarm is not decleared the default is False!')
        else:
            print("We detect status file doesn't exist, I will create it for you :-)")
            with open(self.file_name, 'w') as f:  # TODO Should I use w???
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
                        # finally:
                        #  somethink like ValueError, if ValueError, as... do something
                        #     return False  # Should be a function to rewrite the status file 
                else:
                    print('The File ID is not the same with client')
                    return False
            else:
                print('Error, The file should have only 3 columns')
                return False
            return True