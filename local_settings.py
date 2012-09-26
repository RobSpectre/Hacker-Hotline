'''
Configuration Settings
'''

''' Uncomment to configure using the file.  
WARNING: Be careful not to post your account credentials on GitHub.

TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxx" 
TWILIO_AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
AGENT_NUMBER = "+15558675309"
'''

# Begin Heroku configuration - configured through environment variables.
import os
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'ACxxxxxx')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'yyyyyyyyyy')
TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID', None)
TWILIO_APP_SID = os.environ.get('TWILIO_APP_SID', None)

# Specify the hackers working this hotline by putting their names and phone
# numbers in the list of dictionaries below.
HACKERS = [
    {'name': 'Joey Ramone', 'number': '+15558675309'},
    {'name': 'Johnny Ramone', 'number': '+15556667777'},
    {'name': 'Marky Ramone', 'number': '+15552223333'},
    {'name': 'Dee Dee Ramone', 'number': '+15553334444'}]
