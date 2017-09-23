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
