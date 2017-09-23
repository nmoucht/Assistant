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
    elif (intent == 'yes'):
        action = 'accept'
    elif (intent == 'no'):
        action = 'reject'
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

    highest_convenience_index = -999
    day_block_most_convenient = (
        0, 0) # (day_number, block_number)
    # if highest_convenience_index is below 0, a convenient time was not found

    # iterate through schedule
    day_number = 0
    for block_list in schedule: # block_list is a day in memory
        if day_number < current_day:
            # check only for days in the future
            day_number += 1
            continue
        block_number = 0
        for block in block_list:
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

            if block.get_organizing_data()['available'] == False:
                time_pressure_index = 0
            else:
                time_pressure_index = calculate_time_pressure_index(
                    total_block_distance, organizing_data)

            block_match_index = calculate_block_match_index(
                block, organizing_data)

            convenience_index = time_pressure_index + block_match_index

            if convenience_index > highest_convenience_index:
                highest_convenience_index = convenience_index
                day_block_most_convenient = (day_number, block_number)

            # at the end of the for loop
            block_number += 1
        # at the end of the for loop
        day_number += 1

    if highest_convenience_index > 0:
        return day_block_most_convenient
    else:
        return -1 # no convenient time was found

def calculate_block_match_index(block, organizing_data):
    block_organizing_data = block.get_organizing_data()
    index = 0
    # consider if the block is available
    if block_organizing_data['available'] == False:
        index -= 2

    block_time = block_organizing_data['block_time']
    rejected_blocks = block_organizing_data['blocks_rejected']
    for start, end in rejected_blocks:
        if block_time >= start and block_time < end:
            index -= 1000 # block is rejected!

    index += block_organizing_data['general_priority']

    return index

def calculate_time_pressure_index(time_distance, organizing_data):
    # calculate exponential term with the block_distance (each block = 1hr)
    priority_constant_multiplier = organizing_data['general_priority']
    urgency_base = 5 # very debatable default
    # in infinity term will be 0, which is fine because as long as it isn't
    # incovenient for them to meet, the block match term will be positive
    growth_factor = 0.99

    return (
        priority_constant_multiplier * urgency_base * (growth_factor ** time_distance))
