# This class represents a black-box in an airplane,
# which means data container with all flight parameters
# recorded therein every N seconds

import json
import os


class BlackBox:
    def __init__(self):
        self.filename = "flightData.json"
        self.data = []
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    # reading json file (black-box content)
    def read(self):
        with open(self.filename) as data_file:
            data = [json.loads(line) for line in data_file]
        return data

    # storing single dataset into black-box (json file)
    def save(self, data):
        with open(self.filename, 'a') as outfile:
            json.dump(data, outfile)
            outfile.write(os.linesep)
