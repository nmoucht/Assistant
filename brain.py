# This is a public client access token, when there's a server,
#  this must be changed to a server-side token

from wit import Wit
import inspect
wit_access_token = '746THEHISF2ZB7YSHFMR2WVS6PNIZDJE'

def parse_request(request_text):

    client = Wit(wit_access_token)
    #print(Wit.access_token)
    response = client.message(request_text)
    #"I want to schedule a meeting", verbose=True)

    #client.interactive()

    #print(dir(response))

    # intent is a list, in which the second element is the confidence (0-1)
    intent = response.get('entities').get('intent')[0].get('value')

    # the intended action will be stored here
    action = ''

    if (intent == 'meeting_set'):
        action = 'schedule'
    else:
        print('no action found for intent {}'.format(intent))
        action = None

    return action

# schedule is a Schedule object, time_now is a tuple: (day, block#)
def suggest_time(schedule, time_now, organizing_data):
    # the basic first version of the time suggestion function calculates a
    # how much match there is between block properties and organizing data
    # properties, and adds them to an eponential decay function which tries
    # to fill fast the empty blocks depending on how close they are to today
    current_day, current_block = time_now

    # iterate through schedule
    day_number = 0
    for block_list in schedule:
        if day_number < current_day:
            # check only for days in the future
            day_number += 1
            continue
        block_number = 0
        for block in day:
            if day_number == current_day and block_number < current_block:
                # check only for blocks in the future
                block_number += 1
                continue
            # calculate exponential term of convenience index
            total_block_distance = 0
            total_block_distance += 24 * (day_number - current_day)
            # day_number >= day_index
            total_block_distance += (block_number - current_block)
            # if block_number < current_block, blocks
            # would be substracted, _which is correct_

            # calculate exponential term with the block_distance (each block = 1hr)
            # WIP TODO

            # at the end of the for loop
            block_number += 1
        # at the end of the for loop
        day_number += 1
    print('I suggest 5')
