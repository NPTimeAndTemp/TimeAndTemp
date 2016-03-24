from flask import Flask
from twilio import twiml
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib2

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def voice_response():
    """Respond to incoming requests."""
    resp = twiml.Response()
    # give time
    resp.say(get_datetime(), voice='female', language='us')
    # pause 1 seconds between time and temp
    resp.pause(length=1)
    # give temp
    resp.say(get_weather(), voice='female', language='us')
    return str(resp)


def get_datetime():
    """Get and Build out date time string"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day = now.day
    month = now.month

    if hour >= 13:
     hour -= 12
    period = 'p m'
    elif hour = 12:
     period = 'p m'
    else:
     period = 'a m'

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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
