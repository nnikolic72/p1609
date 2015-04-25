// Heroku issue a command to specific app
heroku <command> --app squaresensor-dev

// Heroku migrate django models
heroku run python manage.py migrate --app squaresensor-dev
heroku run python manage.py migrate --app squaresensor-prod

// collect static files
heroku run python manage.py collectstatic

// Heroku status - you have to be in deployment directory
cd squaresensor
heroku ps
heroku logs

//Heroku environment settings
heroku config:set S3_KEY=8N029N81
heroku config:set DJANGO_SETTINGS_MODULE=squaresensor.settings.test --app squaresensor-dev
heroku config:set DJANGO_SETTINGS_MODULE=squaresensor.settings.prod --app squaresensor-prod
heroku config:set SECRET_KEY="jdsjdsdhsjdh"
heroku config:set IS_APP_LIVE=1 --app squaresensor-dev
heroku config:set IS_PAYMENT_LIVE=1 --app squaresensor-dev

// Needed to set on squaresensor heroku
heroku config:set CLIENT_ID="" --app squaresensor-dev
heroku config:set CLIENT_SECRET="" --app squaresensor-dev
heroku config:set INSTAGRAM_REDIRECT_URI="" --app squaresensor-dev

//Heroku check for problems
heroku run "python manage.py check" --app squaresensor-dev

//Heroku add domain
heroku domains:add www.squaresensor.com --app squaresensor-dev

//Windows Powerhell environment variable setup
$env:DJANGO_SETTINGS_MODULE="nnpicksdj.settings.local"
//Windows cmd
set DJANGO_SETTINGS_MODULE=squaresensor.settings.local

//Heroku maintenace mode
heroku maintenance:on --app squaresensor-prod
heroku maintenance:off --app squaresensor-prod

// heroku Postgress database backup
heroku pg:backups capture --app squaresensor-prod

// requirements.txt - Heroku
1. Add this string without quotes to the end of requrements.txt. "-r requirements_heroku.txt"
2. Convert requirements.txt file in Notepad++ to Encoding > Encode in ANSI

// Hwow to remove already commited file from Git
git rm -r --cached .idea
-> update .gitignore
git commit -m "some text"
git push

// PyCrypto Windows install
easy_install http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe

// Microsoft compiler for Python 2.7
http://www.microsoft.com/en-us/download/details.aspx?id=44266

// Instggram scopes
basic
comments
relationships
likes

// django-import-export
File must be saved in encoding "UTF-8 without BOM"

// RabbitMQ defaults
4369 (epmd), 25672 (Erlang distribution)
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

// Starting Celery
celery -A squaresensor worker -l info
// Starting Celery on Heroku as a worker
worker: celery -A squaresensor worker -l info
// Celery Debugger:
Enable Telnet Client on Windows 
1. Programs and Features > Turn Windows features on or off > Check "Telnet Client", wait to install. No reboot.
2. rdb.set_trace() in tasks.py to enable debugger
3. telnet to opened port, as shown in Celery terminal window

// Group
Inspiring User Editor

// Testing
coverage run manage.py test
coverage html --include=" $ SITE_URL*" --omit="admin.py"