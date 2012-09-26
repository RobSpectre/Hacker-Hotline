import unittest
from mock import patch

from twilio.rest import TwilioRestClient

from .context import app


app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'
app.config['TWILIO_CALLER_ID'] = '+15558675309'

app.twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_AUTH_TOKEN'])

app.config['HACKERS'] = [
    {'name': 'Rob Spectre', 'number': '+15555555555'},
    {'name': 'Caine Tighe', 'number': '+15555555556'},
    {'name': 'Zack Pappis', 'number': '+15555555557'},
    {'name': 'Amit Jotwani', 'number': '+15555555558'},
    {'name': 'Brett Van Zuiden', 'number': '+15555555559'}]


class TwiMLTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def assertTwiML(self, response):
        self.assertTrue("<Response>" in response.data, "Did not find " \
                "<Response>: %s" % response.data)
        self.assertTrue("</Response>" in response.data, "Did not find " \
                "</Response>: %s" % response.data)
        self.assertEqual("200 OK", response.status)

    def sms(self, body, path='/sms', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', extra_params=None):
        params = {
            'SmsSid': 'SMtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'Body': body,
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if extra_params:
            params = dict(params.items() + extra_params.items())
        return self.app.post(path, data=params)

    def call(self, url='/voice', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', extra_params=None):
        params = {
            'CallSid': 'CAtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'CallStatus': 'ringing',
            'Direction': 'inbound',
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if extra_params:
            params = dict(params.items() + extra_params.items())
        return self.app.post(url, data=params)


class TwilioTests(TwiMLTest):
    def test_call(self):
        response = self.call()
        self.assertTwiML(response)
        self.assertTrue("Redirect" in response.data, "Did not find Redirect " \
                "verb, instead got: %s" % response.data)
        self.assertTrue("/caller" in response.data, "Did not get redirected " \
                "to caller endpoint, instead got: %s" % response.data)

    def test_callAsAgent(self):
        response = self.call(from_=app.config['HACKERS'][0]['number'])

        self.assertTwiML(response)
        self.assertTrue("Redirect" in response.data, "Did not find Redirect " \
                "verb, instead got: %s" % response.data)
        self.assertTrue("/agent" in response.data, "Did not get redirected " \
                "to agent endpoint, instead got: %s" % response.data)

    def test_caller(self):
        response = self.call(url='/caller')
        self.assertTwiML(response)
        self.assertTrue("Play" in response.data, "Did not find intro " \
                "statement in response, instead: %s" % response.data)
        self.assertTrue("Enqueue" in response.data, "Did not find Enqueue " \
                "in response, instead: %s" % response.data)


def SmsTests(TwiMLTest):
    @patch('twilio.rest.resources.SmsMessage', autospec=True)
    @patch('twilio.rest.resources.SmsMessages', autospec=True)
    def setUp(self, MockMessages, MockMessage):
        self.app = app.test_client()

        # Set up SMS mocks
        mock_message = MockMessage.return_value
        app.twilio_client.sms.messages = MockMessages.return_value
        app.twilio_client.sms.messages.create.return_value = \
            mock_message

    def test_agent(self):
        response = self.call(url='/agent',
                from_=app.config['HACKERS'][0]['number'])

        self.assertTwiML(response)
        self.assertTrue("Dial" in response.data, "Did not find Dial in the " \
                "agent response, instead: %s" % response.data)
        self.assertTrue(app.twilio_client.sms.messages.create.call_count == 4,
                "Did not send expected four SMS messages, instead sent: %s" %
                app.twilio_client.sms.messages.create.call_count)

    def test_wait(self):
        response = self.call(url='/wait', extra_params={'QueuePosition': '1'})

        self.assertTwiML(response)
        self.assertTrue("Say" in response.data, "Did not find a position " \
                "announcement in wait room, instead: %s" % response.data)
        self.assertTrue("gangnam" in response.data, "THERE WAS NO GANGNAM " \
                "WTF?!?!?! - %s" % response.data)
        self.assertTrue(app.twilio_client.sms.messages.create.call_count == 5,
                "Did not send expected four SMS messages, instead sent: %s" %
                app.twilio_client.sms.messages.create.call_count)

    def test_smsNonAgent(self):
        response = self.sms("test")
        self.assertTwiML(response)
        self.assertTrue("You do not appear" in response.data, "Did not get " \
                "rejection SMS, instead: %s" % response.data)
        self.assertTrue(app.twilio_client.sms.messages.create.call_count == 0,
                "Expected to send no SMS messages, instead sent: %i" %
                app.twilio_client.sms.messages.create.call_count)
