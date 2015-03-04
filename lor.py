import requests
import operator
import os
from flask import Flask, request, render_template, redirect, url_for
from collections import Counter


app = Flask(__name__)
db = Counter()  # todo: sqlite3 db, because view counts don't persist
YOUTUBE_KEY = os.environ.get('YOUTUBE')


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
    return title


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
    yt_id = request.args.get('v')
    db[yt_id] += 1
    top_ten = db.most_common(10)
    titles = {}
    for vid, plays in top_ten:
        titles[get_title(vid)] = plays
    sorted_titles = sorted(titles.items(), key=operator.itemgetter(1))[::-1]
    try:
        related_videos = get_related(yt_id)
    except:
        related_videos = None  # hacky workaround if api key lookup fails
    return render_template('watch.html', yt_id=yt_id, titles=sorted_titles, related=related_videos)


if __name__ == '__main__':
    app.run(debug=True)
