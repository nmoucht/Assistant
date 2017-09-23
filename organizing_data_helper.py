
def get_default():
    return {
        'general_priority': 1, # possible default priority
        'location': (0, 0, 0), # gps coordinates
        'purpose': '', # same as self.purpose. same purpose can
        # be considered same activity and be used to find patterns
        'blocks_rejected': [(0, 16), (36, 48)], # in these blocks he is not available
        'time_ranges_convenience': [], # each element is 3-element tuple,
        # first two elements are start and end, third is convenience
        'available': True,
        'block_time': 0 # when is this block?
    }
