import brain
from schedule import Schedule
import organizing_data_helper

#request = "I want to schedule a meeting"
request = "the meeting will last four and a half hours"
action, info = brain.parse_request(request)

duration = 1
if action == 'set_duration':
    duration = info

print(action, info)
request = "I want to schedule a meeting"
action, info = brain.parse_request(request)

if action == 'schedule':
    current_schedule = Schedule()
    organizing_data = organizing_data_helper.get_default()
    current_time = (2, 16)

    # this block is preferred empty
    current_schedule[2][16].get_organizing_data()['general_priority'] = -1

    suggested_time = brain.suggest_time(current_schedule, current_time, organizing_data, meeting_duration = duration)
    print(suggested_time)
    #print(current_schedule)
