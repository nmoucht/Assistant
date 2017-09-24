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
    entities = response.get('entities')

    intent = ''
    if 'duration' in entities:
        duration_seconds = entities['duration'][0]['normalized']['value']
        # because there are 48 blocks, each block is 30 minutes
        duration_blocks = int(duration_seconds / (30 * 60))
        duration = duration_blocks
        intent = 'duration_set'
    elif 'intent' in entities:
        intent = entities.get('intent')[0].get('value')
    elif 'datetime' in entities:
        try:
            datetime = entities['datetime'][0]['value']
        except Exception:
            print(entities['datetime'][0])
            raise KeyError
        intent = 'date_set'
    elif 'identify' in entities:
        name = entities['identify'][0]['value']
        intent = 'identify'

    # the intended action will be stored here
    action = ''
    info = None

    if (intent == 'meeting_set'):
        action = 'schedule'
    elif (intent == 'yes'):
        action = 'accept'
    elif (intent == 'no'):
        action = 'reject'
    elif (intent == 'duration_set'):
        action = 'set_duration'
        info = duration
    elif (intent == 'date_set'):
        action = 'set_date'
        info = datetime
    elif (intent == 'identify'):
        action = 'identify'
        info = name
    else:
        print('no action found for intent {}'.format(intent))
        action = None

    return (action, info)

# schedule is a Schedule object, time_now is a tuple: (day, block#)
def suggest_time(schedule, time_now, organizing_data, meeting_duration = 1):
    # the basic first version of the time suggestion function calculates a
    # how much match there is between block properties and organizing data
    # properties, and adds them to an eponential decay function which tries
    # to fill fast the empty blocks depending on how close they are to today
    current_day, current_block = time_now

    highest_convenience_index = -999
    starting_day_block_most_convenient = (
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
            if block_number + meeting_duration - 1 > 47:
                # not enough time in a day
                break
            # calculate exponential term of convenience index
            total_block_distance = 0
            total_block_distance += 24 * (day_number - current_day)
            # day_number >= day_index
            total_block_distance += (block_number - current_block)
            # if block_number < current_block, blocks
            # would be substracted, _which is correct_

            total_convenience_index = 0
            for i in range(meeting_duration):
                current_block_distance = total_block_distance + i
                # meeting_block is the block being checked now
                #meeting_block = schedule[day_number][block_number]
                meeting_block = block_list[block_number]
                convenience_index = calculate_convenience_index(
                    current_block_distance, meeting_block, organizing_data)


                total_convenience_index += convenience_index

            convenience_index = total_convenience_index / meeting_duration
            # when meetings last more than one block, the average counts
            if convenience_index > highest_convenience_index:
                highest_convenience_index = convenience_index
                starting_day_block_most_convenient = (day_number, block_number)

            # at the end of the for loop
            block_number += 1
        # at the end of the for loop
        day_number += 1

    if highest_convenience_index > 0:
        return starting_day_block_most_convenient
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
    growth_factor = 0.995

    return (
        priority_constant_multiplier * urgency_base * (growth_factor ** time_distance))

def calculate_convenience_index(total_block_distance, block, organizing_data):
    if block.get_organizing_data()['available'] == False:
        time_pressure_index = 0
    else:
        time_pressure_index = calculate_time_pressure_index(
            total_block_distance, organizing_data)

    block_match_index = calculate_block_match_index(
        block, organizing_data)

    convenience_index = time_pressure_index + block_match_index

    return convenience_index
