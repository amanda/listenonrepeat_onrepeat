# listenonrepeat_onrepeat
clone of listenonrepeat.com

## to use:
1. clone the repo
2. install dependencies with pip: ```pip install -r requirements.txt```
3. setup the database: ```$ python init_db.py```
4. run ```$ python lor.py``` and head to localhost:5000 in your favorite browser
5. optional: for recommended videos to work when running on your local machine, you're going to need to set up a youtube api key as an environment variable. sign up for one [using these instructions](https://developers.google.com/youtube/registering_an_application) and set it as an environment variable: ```$ export YOUTUBE='your api key'```
6. install the bookmarklet (available on the homepage) and click it while on youtube to start that video on repeat, or replace the "youtube.com" part of a youtube URL with "localhost:5000"

## todo:
1. ~~real database like sqlite3 or sqlalchemy, so view counts persist.~~
2. tests
3. ~~recommended videos~~
