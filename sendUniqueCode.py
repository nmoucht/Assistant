import random
import string
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC16a993b38d31bad4cde90d02349b12ef"
auth_token = "049e5e61b3ceffe60551bc3be8b19a81"
client = Client(account_sid, auth_token)

def generatePinCode():
    code=[]
    for x in range(0, 5):
        if x != 4:
            print x
            code.append(random.randint(0, 9))
        else:
            code.append(random.choice(string.letters))
            generatedCode = ''.join( map(str , code))
            return generatedCode

def sendCodeToUser(userPhoneNumber):
    code = generatePinCode()
    message =  client.api.account.messages.create(to=userPhoneNumber,
    from_= "+17329174392",
    to = userPhoneNumber,
    body= "Hi to access the meeting that you booked with Mr.Roshan Rishav, use this pin code " + code)


generatePinCode()
