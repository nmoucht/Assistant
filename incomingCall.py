import random
import string
import organizing_data_helper
from sendUniqueCode import sendCodeToUser, generatePinCode
import makeEvent
#from makeEvent import create_event, get_credentials
from brain import parse_request, suggest_time
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from schedule import Schedule
from pymongo import MongoClient
from flask.ext.pymongo import PyMongo
import datetime
from math import floor


app = Flask(__name__)
mongo = PyMongo(app)
connection = MongoClient("mongodb://ds147544.mlab.com:47544/")
db = connection["userdatabase"]
event_ID = db.event_ID
db.authenticate(name="nikosm",password="Netherlands1")
# Account SID and

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


#
# @app.route("/yesorno", methods=['GET', 'POST'])
# def yesorno(dataType):
#     if ['SpeechResult'] in request.values:
#         if request.values['SpeechResult'] == "Yes.":
#             return true
#         else:
#             return false
#
#
#
# def confirm(dataType, data):
#     resp = VoiceResponse()
#     if dataType == "name":
#         gather = Gather(input='speech dtmf', action='/yesorno')
#         gather.say("Hi, " + data + "Did I say your name right?")
#         resp.append(gather)
#
#         resp.redirect('/confirm')
#         return str(resp)
#     elif dataType == "summary":
#         gather = Gather(input='speech dtmf', action='/yesorno')
#         gather.say("Hi, " + "Is this the right description for your meeting? " + data)
#         resp.append(gather)
#
#         resp.redirect('/confirm')
#     elif dataType == "location":
#         gather = Gather(input='speech dtmf', action='/yesorno')
#         gather.say("Hi, " + "Is this the right location for your meeting? " + data)
#         resp.append(gather)
#
#         resp.redirect('/confirm')
#     elif dataType == "startTime":
#         gather = Gather(input='speech dtmf', action='/yesorno')
#         gather.say("Hi, " + "Is this the right start time for your meeting? " + data)
#         resp.append(gather)
#
#         resp.redirect('/confirm')
#     elif dataType == "endTime":
#         gather = Gather(input='speech dtmf', action='/yesorno')
#         gather.say("Hi, " + "Is this the right end time for your meeting? " + data)
#         resp.append(gather)
#
#         resp.redirect('/confirm')
#
#
#
#
#--DB

def addEventIDtoDatabase(eventID, eventCode):
	eventCode=[("eventCode",eventCode)]
	eventID=[("event_ID",eventID)]
	a={}
	a.update(eventCode)
	a.update(eventID)
	event_ID.insert_one(a)

def deleteEventIDfromDatabase(eventID):
    try:
        print("ID")
        print(eventID)
        deletedID = event_ID.delete_one({ "event_ID": eventID})
        return "Deleted"
    except Exception,e:
        return "ERROR"

def isThereIndex(index):
	x=event_ID.find_one({ "eventCode": index})
	if x is not None:
		print(1)
		return x["event_ID"]
	else:
		print(0)
		return None

def generatePinCode():
    code=[]
    for x in range(0, 4):
        if x != 4:
            print x
            code.append(random.randint(0, 9))
    generatedCode = ''.join( map(str , code))
    return generatedCode

@app.route("/menu", methods=['GET', 'POST'])
def menu():
    resp = VoiceResponse()
    gatherOption = Gather(num_digits=1, action='/decider')
    gatherOption.say("Hi this is Alfred, Press zero, if you want to create a new event, or press 1 if you want to access an old event ")
    resp.append(gatherOption)
    # Start our <Gather> verb

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')
    return str(resp)

@app.route("/decider", methods=['GET', 'POST'])
def decider():
    resp = VoiceResponse()
    if "Digits" in request.values:
        if request.values["Digits"] == '1':
            gather = Gather(num_digits=5, action='/cancelEvent')
            gather.say("Press your event code")
            resp.append(gather)
            return str(resp)
        else:
            resp.redirect('/voice')
            return str(resp)

@app.route("/cancelEvent", methods=['GET', 'POST'])
def cancelEvent():
    resp = VoiceResponse()
    if "Digits" in request.values:
        pin = request.values["Digits"]
        eventId = isThereIndex(pin)
        print(eventId)
        if eventId != "None":
            done = makeEvent.cancel_event(eventId)
            if done == "Cancelled":
                x=deleteEventIDfromDatabase(eventId)
                print(x)
                resp.say("Your event has been cancelled, Have a good day, Bye now!")
                return str(resp)
            else:
                resp.say("It seems that there is no event associated with this pin, Please wait while you are taken back to the main menu")
                resp.redirect('decider')
        else:
            resp.say("It seems that there is no event associated with this pin, Please wait while you are taken back to the main menu")
            resp.redirect('decider')

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()


    #print(request.values["to"])
    # Get the Name of the caller
    gatherName = Gather(input='speech dtmf', action='/summary')
    gatherName.say('Please tell me your name')
    resp.append(gatherName)
    # Start our <Gather> verb

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')
    return str(resp)

@app.route('/summary', methods=['GET', 'POST'])
def gather():
    #"""Save Name, ask summary"""
    # Start our TwiML response
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        detected_action, name = parse_request(request.values['SpeechResult'])
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
        gatherStartTime.say("Thanks, When would you like the meeting to start? For example say 'October 22 2017 3:30 pm' ")
        resp.append(gatherStartTime)
        return str(resp)
    else:
        resp.redirect('/endTime')

@app.route('/endTime', methods=['GET', 'POST'])
def endTime():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        print(request.values['SpeechResult'])
        # startTimeDet = convertToRequiredFormat(request.values['SpeechResult'])
        startTimeDet = parse_request(request.values['SpeechResult'])
        print(startTimeDet[1])
        event['start']['dateTime'] = startTimeDet[1] #adding to the dict
        gatherEndTime = Gather(input='speech dtmf', action='/bookMeeting')
        gatherEndTime.say("Thanks, When would you like the meeting to end? For example say 'October 1 2017 2:00pm' ")
        resp.append(gatherEndTime)
        return str(resp)
    else:
        resp.redirect('/endTime')

@app.route('/bookMeeting', methods=['GET', 'POST'])
def bookMeeting():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        endTimeDet =  parse_request(request.values['SpeechResult'])
        print(endTimeDet[1])
        event['end']['dateTime'] = endTimeDet[1] #adding to the dict
        resp.say("Please wait while I book your meeting")
        CalendarResponse = makeEvent.create_event(event)
        print(CalendarResponse)
        if CalendarResponse != 'Busy':
            code = sendCodeToUser(request.values['From'])
            eventId = CalendarResponse[0]
            addEventIDtoDatabase(eventId, code)
            resp.say("Great! Your meeting has been booked")
            return str(resp)
        else:
            gather = Gather(input='speech dtmf', action='/getSuggestion')
            gather.say("It seems that the time is not free, Do you want me to suggest you a time?")
            resp.append(gather)
            return str(resp)
            print(event)
            return str("Based on Google api return")
    else:
        resp.say("Something Happened, Please wait")
        resp.redirect('/endTime')
    # If Twilio's request to our app included already gathered digits,
    # process them
@app.route('/getSuggestion', methods=['GET', 'POST'])
def getSuggestion():
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        needSuggestion = request.values['SpeechResult']
        if (needSuggestion == "Yes.") or (needSuggestion == "Yes") or (needSuggestion == "yes." or (needSuggestion == "yes") or (needSuggestion == "sure"))  :
            hasPickedDay=False
            #schedule=Schedule()
            schedDict=makeEvent.fourteen_day_schedule()
            schedule = makeEvent.convert_time_to_block(schedDict)
            sched=Schedule()
            utc_datetime = datetime.datetime.utcnow()
            currentTime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
            time_now = makeEvent.convert_input_time_to_block(currentTime)

            # # fill the schedule with the schedule downloaded from GCalendar
            organizing_data = organizing_data_helper.get_default()
            # # fill the organizing_data with the event data that we have
            # time_now = (0, 0)# WRONG, should have current time
            # meeting_duration = 1 #WRONG, should contain meeting duration
            print("hello")
            suggested_time = suggest_time(
             sched, time_now, organizing_data, 1)
            day, block=suggested_time
            print(day)
            print(block)
            monthlist=["January","February","March","April","May","June","July","August","September","October","November","December"]
            monthlistLength=[31,28,31,30,31,30,31,31,30,31,30,31]
            monthIndex=int(currentTime[currentTime.index("-")+1:currentTime.index("-")+3])+1
            currentMonth=monthlist[monthIndex]
            daySuggest=int(currentTime[6:7])+day
            if(daySuggest>monthlistLength[monthIndex]):
                monthIndex+=1
                currentMonth=monthlist[monthIndex]
                daySuggest-=monthlistLength[monthIndex-1]
            time=block*0.5
            hour=floor(time/24)
            minutes=(time-hour)*60
            print(hour)
            print(minutes)
            timeMornorEve="am"
            if(hour>12):
                timeMornorEve="pm"
                hour-=12
            elif(hour==12):
                timeMornorEve="pm"
            strDate="A suggested date is "+str(currentMonth)+" "+str(daySuggest)+" 2017 at "+str(hour)+":"+str(minutes)+ " "+timeMornorEve
            startDate=str(currentMonth)+" "+str(daySuggest)+" 2017 at "+str(hour)+":"+str(minutes)+ " "+timeMornorEve
            print(strDate)
            enDate= str(currentMonth)+" "+str(daySuggest)+" 2017 at "+str(hour + 1) +":"+str(minutes)+ " "+timeMornorEve
            resp.say(strDate)
            resp.say("Is this time ok with you?")
            resp = VoiceResponse()
            if 'SpeechResult' in request.values:
                yesOrNo = request.values['SpeechResult']
                if (needSuggestion == "Yes.") or (needSuggestion == "Yes") or (needSuggestion == "yes." or (needSuggestion == "yes") )  :

                        #create event
                    time_in_service = parse_request(startDate)
                    endTime_in_service = parse_request(enDate)
                    event['start']['dateTime'] = time_in_service[1]
                    event['end']['dateTime'] = endTime_in_service[1]

                    makeEvent.create_event(event)
                    hasPickedDay=True
                    resp.say("Cool, Your meeting has been booked. Have a nice day")
                else:
                    resp.say("Bye, have a nice day!")
                        #add rejected time to rejected_times

            # # check if he's fine, if he's not, add to rejected_times
            # # in organizing_data the time that he rejected

                #print("Make Suggestions")
            return str(resp)

        else:
            resp.say("No Problem, Have a good day ahead!")
            return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
