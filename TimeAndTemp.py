from flask import Flask
from twilio import twiml
from datetime import datetime
import pytz
import xml.etree.ElementTree as ET
import urllib2
from os import path, getenv
from Dates import Dates

app = Flask(__name__)
port = int(getenv('VCAP_APP_PORT', 8080))

@app.route("/", methods=['GET', 'POST'])
def voice_response():
    """Respond to incoming requests."""
    resp = twiml.Response()
    # play ad
    resp.play(get_intro())
    # give time
    resp.say(get_datetime(), voice='alice', language='us')
    # pause 1 seconds between time and temp
    resp.pause(length=1)
    # give temp
    resp.say(get_weather(), voice='alice', language='us')
    return str(resp)


def get_datetime():
    """Get and Build out date time string"""
    local_tz = pytz.timezone('US/Central')
    # set now as current time
    now = datetime.now()
    now = now.replace(tzinfo=pytz.utc).astimezone(local_tz)
    # set and format hour month and period (am/pm)
    hour = datetime.strftime(now, '%I')
    month = datetime.strftime(now, '%B')
    period = datetime.strftime(now, '%p')

    minute = now.minute
    # uses dates dict in dates file to change int day to ordinal
    day = Dates.get(now.day)

    if minute == 0:
        minute = 'o clock'
    elif minute < 10:
        minute = 'o {}'.format(minute)
    else:
        pass

    # builds time string
    time_str = 'Today is {} {}. The current time is {} {} {}. '.format(month, day, hour, minute, period)

    return str(time_str)


def get_weather():
    """Get and build out weather string. Uses NOAA XML."""
    # gets weather xml from noaa web. should replace KLBF with local call site.
    weather_xml = urllib2.urlopen('http://w1.weather.gov/xml/current_obs/KLBF.xml')
    # open xml
    weather_tree = ET.ElementTree(file=weather_xml)
    weather_root = weather_tree.getroot()
    # current temp in F is located at 13. should make dynamic.
    curr_temp = weather_root[13].text
    # decimal precision is not necessary. strips to only whole number.
    curr_temp = str(curr_temp).rpartition('.')[0]

    # build string for temp
    temp_str = 'The current temperature is {} degrees.'.format(curr_temp)
    return str(temp_str)


def get_intro():
    """Returns mp3 add to play at intro."""
    # check to see if file exists
    if path.isfile('./static/intro/Intro.mp3'):
        return './static/intro/Intro.mp3'
    # if the file doesn't exist, one wait tone will be passed
    else:
        return 'digits = "w"'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)
