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

// requirements.txt - Heroku
1. Add this string without quotes to the end of requrements.txt. "-r requirements_heroku.txt" 2. Convert requirements.txt file in Notepad++ to Encoding > Encode in ANSI

// Hwow to remove already commited file from Git
git rm -r --cached .idea
-> update .gitignore
git commit -m "some text"
git push
