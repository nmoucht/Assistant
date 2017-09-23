# the information that one block in the calendar will contain

class Block:
    def __init__(self):
        self.purpose = ''
        self.comments = ''
        self.location = ''
        self.organizing_data = {
            'priority': 1, # possible default priority
            'location': (0, 0, 0), # gps coordinates
            'purpose': '', # same as self.purpose. same purpose can
            # be considered same activity and be used to find patterns
            'blocks_rejected': [], # in these blocks he is not available
            'time_ranges_convenience': [] # each element is 3-element tuple,
            # first two elements are start and end, third is convenience
        }

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
