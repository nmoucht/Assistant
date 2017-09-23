# the information that one block in the calendar will contain

import organizing_data_helper

class Block:
    def __init__(self):
        self.purpose = ''
        self.comments = ''
        self.location = ''
        self.available = True
        self.organizing_data = organizing_data_helper.get_default()

    def get_purpose(self):
        return self.purpose

    def get_comments(self):
        return self.comments

    def get_location(self):
        return self.location

    def get_organizing_data(self):
        return self.organizing_data

    def __repr__(self):
        return str(self.organizing_data)
