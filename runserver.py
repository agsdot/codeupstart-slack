from flask import Flask, render_template, request, session
import cgi
import datetime
import time
import json

app = Flask(__name__)

DEBUG=True

app.config['DEBUG'] = True
app.config['PUSHER_CHAT_APP_ID'] = '208257'
app.config['PUSHER_CHAT_APP_KEY'] = '6477030af00c13b1ff9f'
app.config['PUSHER_CHAT_APP_SECRET'] = '8f5c28dbcaa1ebe7d517'
app.config['SECRET_KEY']="\xcb\n\x84\xae\xf5\x8e\xe7\x10;\xd5\x97',u\xff\xe04\xd5\xa5~TRj\xb7"

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

@app.route('/setname/', methods=['POST'])
def set_name():
    session['name'] = request.form['name']

    return "Successful"

@app.route('/pusher/auth/', methods=['POST'])
def pusher_authentication():
    auth = pusher_client.authenticate(
        channel=request.form['channel_name'],
        socket_id=request.form['socket_id'],
        custom_data= {
            'user_id' : session['name']
        }
    )
    return json.dumps(auth)

@app.route("/messages/", methods=['POST'])
def new_message():
    name = request.form['name']
    text = cgi.escape(request.form['text'])
    channel = request.form['channel']

    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple()) * 1000
    pusher_client.trigger("presence-" + channel, 'new_message', {
        'text': text,
        'name': name,
        'time': timestamp
    })

    return "Successful"

if __name__ == "__main__":
    app.run()
