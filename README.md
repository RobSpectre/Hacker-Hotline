# Hacker Hotline 

A nifty [Twilio](http://www.twilio.com) app that sets up a Hacker Hotline powered by
[Twilio Queue](http://www.twilio.com/docs/api/twiml/queue) - get connected with
a hacker when you need programming help.

Built for [PennApps 2012 Fall hackathon](http://www.pennapps.com), Hacker
Hotline creates an easy way for hackathon participants to get help during the
event by setting up a Twilio phone number.  When participants dial in, they
are placed on hold while all the mentor hackers for the event are notified via
SMS.

A hacker responding to that notification is then connected with the first person
waiting in the queue, while all other hackers working the hotline are notified
that the caller was helped.

Super useful for hackathons and other builder events where participants need to
get help from mentors synchronously.

btw - if you're looking for more creative uses of Twilio, I'm dropping a lot of
dirty science in mid-October at [Twiliocon](http://www.twilio.com/conference).

[Hit me up](mailto:rob@twilio.com) if you'd like a deep discount.


[![Build
Status](https://secure.travis-ci.org/RobSpectre/Hacker-Hotline.png)]
(http://travis-ci.org/RobSpectre/Hacker-Hotline)


## Features

Buckle up, snacky.  Hacker Hotline gots some features.

* _Caller Handling_ - Place callers who need help in a queue to be worked by
  hackers staffing the hotline.  
* _Agent Handling_ - Notify hackers of callers who need help via SMS and 
  connect them with the first person in the queue when they call.
* _Easy Deployment_  - Easy tools and instructions for running this app on
  [Heroku](http://www.heroku.com).
* _Automagic Configuration_ - Just run `python configure.py --account_sid ACxxxx --auth_token yyyyy -n -N` 
  this app will configure Twilio and Heroku for you.
* _Testing_ - Cause you have no business helping other hackers if you ship
  without a test suite.
* _[PEP8](http://www.python.org/dev/peps/pep-0008/)_ - The way the good Lord
  intended.

## Usage

Install using the Getting Started instructions below.

Once deployed, configure any Twilio number with the Voice Request URL you find
when you visit your deployed hotline:

![Success
page](https://raw.github.com/RobSpectre/Hacker-Hotline/master/static/images/screenshot.png)

From there, you can configure a Twilio phone number to serve as your hotline.
Once you have set your Voice Request URL, be sure to update your app's
`local_settings` to use this number so the hackers working the queue can receive
notifications.

Additionally, if you can create a separate toll-free number for
callers only, set the Voice Request URL of the toll-free number to the
`/caller` endpoint to connect the number directly to the hotline's Queue.


## Installation

Step-by-step on how to deploy, configure and develop the Hacker Hotline

### Getting Started 

0) Get the requirements:

* [git](http://git-scm.com/)
* [Heroku Toolbelt](https://toolbelt.heroku.com/)
* [Python](http://python.org/download/)

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Hacker-Hotline.git 
</pre>

2) Configure `local_settings.py` with a list of the hackers working your
hotline.

```python
HACKERS = [
    {'name': 'Joey Ramone', 'number': '+15558675309'},
    {'name': 'Johnny Ramone', 'number': '+15556667777'},
    {'name': 'Marky Ramone', 'number': '+15552223333'},
    {'name': 'Dee Dee Ramone', 'number': '+15553334444'}]
```

3) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create
</pre>

4) Deploy to Heroku
<pre>
git push heroku master
</pre>

5) Scale your dynos
<pre>
heroku scale web=1
</pre>

6) Visit the home page of your new Heroku app to find the next configuration
steps!
<pre>
heroku open
</pre>

7) Configure your hotline so your hackers can get notified of incoming calls
using the steps below!


### Configuration

Configure your hotline with three easy options.

#### Automagic Configuration

This hotline ships with an auto-configure script that will create a new TwiML
app, purchase a new phone number, and set your Heroku app's environment
variables to use your new settings.  Here's a quick step-by-step:

1) Make sure you have all dependencies installed
<pre>
make init
</pre>

2) Run configure script and follow instructions.
<pre>
python configure.py --account_sid ACxxxxxx --auth_token yyyyyyy
</pre>

3) For local development, copy/paste the environment variable commands the
configurator provides to your shell.
<pre>
export TWILIO_ACCOUNT_SID=ACxxxxxx
export TWILIO_AUTH_TOKEN=yyyyyyyyy
export TWILIO_APP_SID=APzzzzzzzzzz
export TWILIO_CALLER_ID=+15556667777
</pre>

Automagic configuration comes with a number of features.  
`python configure.py --help` to see them all.


#### local_settings.py

local_settings.py is a file available in the hotline route for you to configure
your twilio account credentials manually.  Be careful not to expose your Twilio
account to a public repo.

```python
ACCOUNT_SID = "ACxxxxxxxxxxxxx" 
AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
```

#### Setting Your Own Environment Variables

The configurator will automatically use your environment variables if you
already have a TwiML app and phone number you would prefer to use.  When these
environment variables are present, it will configure the Twilio and Heroku apps
all to use the hotline.

1) Set environment variables locally.
<pre>
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyy
export TWILIO_APP_SID=APzzzzzzzzzzzzzzzzzz
export TWILIO_CALLER_ID=+15556667777
</pre>

2) Run configurator
<pre>
python configure.py
</pre>


### Development

Getting your local environment setup to work with this hotline is similarly
easy.  After you configure your hotline with the steps above, use this guide to
get going locally:

0) Get the requirements:

* [git](http://git-scm.com/)
* [Python](http://python.org/download/)
* pip
* Foreman

1) Install the dependencies.
<pre>
make init
</pre>

2) Launch local development webserver.
<pre>
foreman start
</pre>

3) Open browser to [http://localhost:5000](http://localhost:5000).

4) Tweak away on `app.py`.


## Testing

This hotline comes with a full testing suite ready for nose.

<pre>
make test
</pre>


## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 

[![githalytics.com
alpha](https://cruel-carlota.pagodabox.com/c24dd158e00552ddc381d60e661ba6e6
"githalytics.com")](http://githalytics.com/RobSpectre/Hacker-Hotline)
