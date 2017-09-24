# just a 2d array with some custom methods
from block import Block
import datetime

def day_block_to_date_string(day_block):
    day, block = day_block
    # the origin is always today (at least now that's the case)
    origin_date = datetime.date.today()
    # this way removes time
    origin_datetime = datetime.datetime(
        origin_date.year, origin_date.month, origin_date.day)

    timedelta = datetime.timedelta(days = day, minutes = block * 30)

    event_datetime = origin_datetime + timedelta
    datetime_pretty_string = event_datetime.strftime(
        '%A %d of %B at %H:%M %p')
    return datetime_pretty_string

class Schedule:
    def __init__(self):
        self.contents = []
        self.add_day(60) # add a year in advance

    def add_day(self, days_to_add = 1):
        for i in range(days_to_add):
            blocks_per_day = 48
            block_list = []
            for j in range(blocks_per_day):
                block = Block()
                block.get_organizing_data()['block_time'] = j + 1
                block_list.append(block)
            self.contents.append(block_list)# 24 blocks of one hour

    def __getitem__(self, key):
        return self.contents[key]

    def __setitem__(self, key, value):
        self.contents[key] = value

    def __repr__(self):
        return str(self.contents)

    def __iter__(self):
        for block_list in self.contents:
            yield block_list
