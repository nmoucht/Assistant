import brain
from schedule import Schedule

action = brain.parse_request("I want to schedule a meeting")

print(action)

current_schedule = Schedule()
print(current_schedule)
