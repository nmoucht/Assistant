# just a 2d array with some custom methods
from block import Block

class Schedule:
    def __init__(self):
        self.contents = []
        self.add_day(365) # add a year in advance

    def add_day(self, days_to_add = 1):
        for i in range(days_to_add):
            blocks_per_day = 24
            block_list = []
            for j in range(blocks_per_day):
                block_list.append(Block())
            self.contents.append(block_list)# 24 blocks of one hour

    def __getitem__(self, key):
        return self.contents[key]

    def __setitem__(self, key, value):
        self.contents[key] = value

    def __repr__(self):
        return str(self.contents)
