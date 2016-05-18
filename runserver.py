from flask import Flask, render_template, request
import cgi
import datetime
import time

app = Flask(__name__)

DEBUG=True

app.config['DEBUG'] = True
app.config['PUSHER_CHAT_APP_ID'] = '208257'
app.config['PUSHER_CHAT_APP_KEY'] = '6477030af00c13b1ff9f'
app.config['PUSHER_CHAT_APP_SECRET'] = '8f5c28dbcaa1ebe7d517'

import pusher

pusher_client = pusher.Pusher(
  app_id=app.config['PUSHER_CHAT_APP_ID'],
  key=app.config['PUSHER_CHAT_APP_KEY'],
  secret=app.config['PUSHER_CHAT_APP_SECRET'],
  ssl=True
)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/messages/", methods=['POST'])
def new_message():
    name = request.form['name']
    text = cgi.escape(request.form['text'])
    channel = request.form['channel']

    now = datetime.datetime.now()
    timestamp = time.mktime(now.tinetuple()) * 1000
    pusher_client.trigger(channel, 'new_message', {
        'text': text,
        'name': name,
        'time': timestamp
    })

    return "Successful"

if __name__ == "__main__":
    app.run()
