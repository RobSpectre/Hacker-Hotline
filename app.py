import os

from flask import Flask
from flask import request
from flask import url_for
from flask import render_template

from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio.util import TwilioCapability


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')
app.twilio_client = TwilioRestClient(
        app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_AUTH_TOKEN'])

# Route incoming callers listed in local_settings to agent endpoint.  
# Otherwise, place them in the queue. 
@app.route('/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    hacker  = getHacker(request)
    if hacker:
        response.redirect("/agent")
    else:
        response.redirect("/caller")
    return str(response)


# Make this route the Voice Request URL to a toll-free Twilio number
# to accept incoming calls from people needing help.
# Props to Caine Tighe from DuckDuckGo for providing the excellent intro voice.
@app.route('/caller', methods=['POST'])
def caller():
    response = twiml.Response()
    response.play("/static/sounds/intro.mp3")
    response.enqueue("Hacker Hotline", waitUrl='/wait')
    return str(response)


# Create waiting room to notify user of current position in the queue and
# play the sweet, soothing sounds of Twilio's coffeeshop collection.
@app.route('/wait', methods=['POST'])
def wait():
    response = twiml.Response()
    response.say("You are number %s in line." % request.form['QueuePosition'])
    response.play("http://demo.brooklynhacker.com/sounds/gangnamstyle.mp3")
    response.redirect(url_for('.wait', _external=True))

    if "client" in request.form['From']:
        location = "the website"
    else:
        if request.form['FromCity']:
            location = "%s, %s at %s" % (request.form['FromCity'],
                request.form['FromState'], request.form['From'])
        else:
            location = "%s at %s" % (request.form['FromCountry'],
                    request.form['FromState'])

    sendSmsToHackers("A hacker is calling from %s." % location)

    return str(response)


# Make this route the Voice Request URL to a regular Twilio number
# for hackers working the hotline to connect with people in the Queue
# who need help.
@app.route('/agent', methods=['POST'])
def agent():
    response = twiml.Response()
    with response.dial() as dial:
        dial.queue("Hacker Hotline")
    hacker = getHacker(request)
    if hacker:
        sendSmsToHackers("%s answered the last caller." % hacker['name'],
                omit=hacker['number'])
    return str(response)


# Enable group messaging for hackers working the hotline to chat.
@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    hacker = getHacker(request)
    if hacker:
        sendSmsToHackers("%s: %s " % (agent['name'], request.form['Body']),
                omit=agent['number'])
    else:
        response.sms("You do not appear to be working the hotline at this " \
                "time.")
    return str(response)


# Couple utility functions to keep controllers DRY.
def getHacker(request):
    for hacker in app.config['HACKERS']:
        if request.form['From'] == hacker['number']:
            return hacker
    return None


def sendSmsToHackers(body, omit=None):
    messages = []
    for hacker in app.config['HACKERS']:
        if hacker['number'] != omit:
            messages.append(app.twilio_client.sms.messages.create(
                to=hacker['number'],
                from_=app.config['TWILIO_CALLER_ID'],
                body=body))
    return messages


# Web page for the Hacker Hotline, allowing users to call in without using a
# phone.
@app.route('/client')
def client():
    configuration_error = None
    for key in ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_APP_SID',
            'TWILIO_CALLER_ID'):
        if not app.config[key]:
            configuration_error = "Missing from local_settings.py: " \
                    "%s" % key
            token = None
    if not configuration_error:
        capability = TwilioCapability(app.config['TWILIO_ACCOUNT_SID'],
            app.config['TWILIO_AUTH_TOKEN'])
        capability.allow_client_incoming("joey_ramone")
        capability.allow_client_outgoing(app.config['TWILIO_APP_SID'])
        token = capability.generate()
    return render_template('client.html', token=token,
            configuration_error=configuration_error)


# Installation screen
@app.route('/')
def index():
    params = {
        'Voice Request URL for Both - use this for one number': url_for('.voice', _external=True),
        'Voice Request URL for Callers - use this for toll-free numbers': url_for('.caller', _external=True),
        'Voice Request URL for Hackers - use this for SMS-enabled numbers': url_for('.agent', _external=True),
        'Client URL - use this for people to call-in using their browsers': url_for('.client', _external=True)}
    return render_template('index.html', params=params)



# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
