import brain
from schedule import Schedule
import organizing_data_helper

request = "I want to schedule a meeting"

action = brain.parse_request(request)

print(action)

if action == 'schedule':
    current_schedule = Schedule()
    organizing_data = organizing_data_helper.get_default()
    current_time = (2, 8)

    # this block is preferred empty
    current_schedule[2][8].get_organizing_data()['general_priority'] = -1

    suggested_time = brain.suggest_time(current_schedule, current_time, organizing_data)
    print(suggested_time)
    #print(current_schedule)
