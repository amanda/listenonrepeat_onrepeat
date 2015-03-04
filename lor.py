import sqlite3
import os
import requests
import operator
from flask import Flask, request, g, render_template, redirect, url_for
from contextlib import closing

DATABASE = 'videos.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
YOUTUBE_KEY = os.environ.get('YOUTUBE')

app = Flask(__name__)
app.config.from_object(__name__) # switch to config.py file later

# db setup
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# routing and helper functions
def get_related(yt_id):
    r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId=' +
                     yt_id + '&type=video&key=' + YOUTUBE_KEY)
    related = r.json()
    videos = {related['items'][i]['id']['videoId']: related['items'][i]['snippet']['title'] for i in range(len(related))}
    return videos


def get_title(yt_id):
    '''(str) -> str,
    takes a youtube ID and returns the video title from JSON from the youtube API'''
    r = requests.get(
        'http://gdata.youtube.com/feeds/api/videos/' + yt_id + '?v=2&alt=jsonc')
    title = r.json()['data']['title']
    return str(title)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watch', methods=['GET', 'POST'])
def show_video():
    '''gets the youtube id from the URL query params and
    1. adds it to the db and increases play count by 1
    2. passes it to the template js to show that video,
    3. gets the top 10 videos by play count to pass to the template
    4. gets related videos'''
    yt_id = str(request.args.get('v'))
    yt_title = get_title(yt_id)
    g.db.execute("INSERT OR REPLACE INTO videos (ytid, title, plays) VALUES (?, ?, (SELECT plays FROM videos WHERE ytid = ?) + 1)", [yt_id, yt_title, yt_id])
    g.db.commit()
    cur = g.db.execute('SELECT title, plays FROM videos ORDER BY plays DESC LIMIT 10')
    top_ten = [dict(title=row[0], plays=row[1]) for row in cur.fetchall()]
    print top_ten

    try:
        related_videos = get_related(yt_id)
    except:
        related_videos = None  # hacky workaround if api key lookup fails
    return render_template('watch.html', yt_id=yt_id, titles=top_ten, related=related_videos)


if __name__ == '__main__':
    app.run(debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)

