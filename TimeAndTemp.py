from flask import Flask
from twilio import twiml
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])

def voice_response():
    """Respond to incoming requests."""
    resp = twiml.Response()
    resp.say(get_datetime())

    return str(resp)


def get_datetime():
    """Get and Build out date time string"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day = now.day
    month = now.month

    if hour > 12:
        hour -= 12
        period = 'p m'
    else:
        period = 'a m'
        pass

    time_srt = 'Today is {} {}. The current time is {} {} {}'.format(month, day, hour, minute, period)

    return str(time_srt)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

