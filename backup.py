import random
import string
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)
event = {
  'summary': '',
  'location': '',
  'description': '',
  'start': {
    'dateTime': '',
    'timeZone': 'America/New_York',
  },
  'end': {
    'dateTime': '',
    'timeZone': 'America/New_York',
  }
 }

@app.rout("/yesorno", methods=['GET', 'POST'])
def yesorno(dataType):
    if ['SpeechResult'] in request.values:
        if request.values['SpeechResult'] == "Yes.":
            return true
        else:
            return false



def confirm(dataType, data):
    resp = voiceResponse()
    if dataType == "name":
        gather = Gather(input='speech dtmf', action='/yesorno')
        gather.say("Hi, " + data + "Did I say your name right?")
        resp.append(gather)

        resp.redirect('/confirm')
        return str(resp)
    elif dataType == "summary":
        gather = Gather(input='speech dtmf', action='/yesorno')
        gather.say("Hi, " + "Is this the right description for your meeting? " + data)
        resp.append(gather)

        resp.redirect('/confirm')
    elif dataType == "location":
        gather = Gather(input='speech dtmf', action='/yesorno')
        gather.say("Hi, " + "Is this the right location for your meeting? " + data)
        resp.append(gather)

        resp.redirect('/confirm')
    elif dataType == "startTime":
        gather = Gather(input='speech dtmf', action='/yesorno')
        gather.say("Hi, " + "Is this the right start time for your meeting? " + data)
        resp.append(gather)

        resp.redirect('/confirm')
    elif dataType == "endTime":
        gather = Gather(input='speech dtmf', action='/yesorno')
        gather.say("Hi, " + "Is this the right end time for your meeting? " + data)
        resp.append(gather)

        resp.redirect('/confirm')





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
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    generatePinCode()
    resp = VoiceResponse()

    # Get the Name of the caller
    gatherName = Gather(input='speech dtmf', action='/summary')
    gatherName.say('Hi this is Roshan\'s assistant, Please tell me your name')
    resp.append(gatherName)
    # Start our <Gather> verb

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')
    return str(resp)

@app.route('/summary', methods=['GET', 'POST'])
def gather():
    """Save Name, ask summary"""
    # Start our TwiML response
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        name = request.values['SpeechResult']
        #---Check Correctness---#
        isCorrect = confirm("name", name)
        if isCorrect == true:
            print(name) #Check
            gatherSummary = Gather(input = 'speech dtmf', action='/location')
            gatherSummary.say("Hi " + name + "Could you specify the reason for the meeting please?")
            resp.append(gatherSummary)
            return str(resp)
    else:
        resp.redirect('/voice')

@app.route('/location', methods=['GET', 'POST'])
def location():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        sumLong = request.values['SpeechResult']
        is
        print(sumLong)
        event['summary'] = sumLong #adding to the dict
        gatherLocation = Gather(input='speech dtmf', action='/startTime')
        gatherLocation.say("Thanks, Can you tell me the location of the meeting?")
        resp.append(gatherLocation)
        return str(resp)
    else:
        resp.redirect('/location')


@app.route('/startTime', methods=['GET', 'POST'])
def startTime():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        locationDet = request.values['SpeechResult']
        print(locationDet)
        event['location'] = locationDet #adding to the dict
        gatherStartTime = Gather(input='speech dtmf', action='/endTime')
        gatherStartTime.say("Thanks, When would you like the meeting to start? For example say '22nd Oct 2017, 2 PM' ")
        resp.append(gatherStartTime)
        return str(resp)
    else:
        resp.redirect('/endTime')

@app.route('/endTime', methods=['GET', 'POST'])
def endTime():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        startTimeDet = convertToRequiredFormat(request.values['SpeechResult'])
        print(startTimeDet)
        event['start']['dateTime'] = startTimeDet #adding to the dict
        gatherEndTime = Gather(input='speech dtmf', action='/bookMeeting')
        gatherEndTime.say("Thanks, When would you like the meeting to end? For example say '4 PM' ")
        resp.append(gatherEndTime)
        return str(resp)
    else:
        resp.redirect('/endTime')

@app.route('/bookMeeting', methods=['GET', 'POST'])
def bookMeeting():
    resp = VoiceResponse(action='/sendConfirmationText')
    if 'SpeechResult' in request.values:
        endTimeDet = convertToRequiredFormat(request.values['SpeechResult'])
        print(endTimeDet)
        event['end']['dateTime'] = endTimeDet #adding to the dict
        resp.say("Please wait while I book your meeting")
        #Make the google api call and wait for a response
        #done = bookMeeting(event)
        if !done:
            sendCodeToUser(request.values['From'])
        else:
            #ask The grid to suggest the best time possible
            #make a new convo session
        print(event)
        return str("Based on Google api return")

    else:
        resp.say("Something Happened, Please wait")
        resp.redirect('/endTime')
    # If Twilio's request to our app included already gathered digits,
    # process them



if __name__ == "__main__":
    app.run(debug=True)
