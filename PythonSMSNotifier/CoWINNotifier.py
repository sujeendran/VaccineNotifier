import os
import requests
from datetime import date, datetime, timezone
import json
from twilio.rest import Client
# Use time modules sleep function if not using Task Scheduler
# to check every 5 mins in a while loop
# import time

_DEBUG_ = False

# SETUP
script_path = os.path.realpath(os.path.dirname(__file__))
debug_pin_response_path = os.path.join(script_path, 'CBPResp.json')
debug_district_response_path = os.path.join(script_path, 'CBDResp.json')
log_path = os.path.join(script_path, 'notifier_log.txt')
# TWILIO DETAILS
TWILIO_NUM = "<YOUR TWILIO PHONE NUMBER>"
ACCOUNT_SID = "<YOUR TWILIO ACCOUNT SID>"
ACCOUNT_TOKEN = "<YOUR TWILIO ACCOUNT SID>"
PERSONAL_NUM = "<YOUR TWILIO REGISTERED NUMBER THAT WILL RECEIVE ALERTS"
client = Client(ACCOUNT_SID, ACCOUNT_TOKEN)
# Number of hours to wait after sending a SMS before sending again
# Depending on your type of account, this may be necessary to reduce cost
SMS_INTERVAL = 3
# LOCATION BASED ON COWIN DETAILS. Refer to README.md in this folder.
STATE_ID = 17
DISTRICT_ID = 308
PINCODE = 678001

def generateCBDQuery(district_id):
    todayDate = date.today()
    formattedDate = todayDate.strftime("%d-%m-%Y")
    query = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={formattedDate}"
    return query

def generateCBPQuery(pincode):
    todayDate = date.today()
    formattedDate = todayDate.strftime("%d-%m-%Y")
    query = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={formattedDate}"
    return query

content = None
if not _DEBUG_:
    session = requests.Session()
    # Mimic browser config
    session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    # By Distric
    # response = session.get(generateCBDQuery(DISTRICT_ID))
    # By Pincode
    response = session.get(generateCBPQuery(PINCODE))
    # print(response.status_code)
    content = json.loads(response.content)
    # print(json.dumps(content, indent=1))
elif _DEBUG_:
    print("***RUNNING IN DEBUG MODE***")
    with open(debug_pin_response_path,'r') as f:
        data = f.readline()
        content = json.loads(data)
    # print(json.dumps(content, indent=1))

print(f"Found {len(content['centers'])} centers in the region")
slots_available = []
for c in content['centers']:
    for s in c['sessions']:
        if s['available_capacity'] > 0:
            slots_available.append(f"{s['date']},{c['name']},Slots:{s['available_capacity']},Age:{s['min_age_limit']}+")
if len(slots_available) > 0:
    print(f"{len(slots_available)} slots available this week:")
    result_string = '\n'.join(slots_available)
    print(result_string)
    current_time = datetime.now(timezone.utc)
    last_msg_time = client.messages.list(limit=1)[0].date_sent
    hours_since_last = (current_time-last_msg_time).seconds//3600
    # SMS only if last message was sent over 3 hours ago
    if hours_since_last > SMS_INTERVAL:
        message = client.messages.create(
                        body =  result_string,
                        from_ = TWILIO_NUM,
                        to =    PERSONAL_NUM)
        print(f"SMS with ID {message.sid} sent to {PERSONAL_NUM}")
    else:
        print(f"SMS not sent as last message was sent within the set {SMS_INTERVAL} hours.")
else:
    print("No free slots in these centers for this week")
with open(log_path,'a') as f:
    f.write(f'Status at {datetime.now()}. Found {len(slots_available)} slots.\n')