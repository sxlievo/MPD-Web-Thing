from flask import Flask, jsonify, render_template
from mpd import MPDClient

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/current_song')
def current_song():
    client = MPDClient()
    client.timeout = 10
    client.connect("localhost", 6600)

    song = client.currentsong()
    status = client.status()
    
    output = {
        "current_song": song,
        "elapsed_time": status.get("elapsed", 0),
        "duration": song.get("duration", 0)
    }

    client.close()
    client.disconnect()

    return jsonify(output)

@app.route('/control_music/<action>', methods=['POST'])
def control_music(action):
    client = MPDClient()
    client.timeout = 10
    client.connect("localhost", 6600)

    if action == 'play':
        client.play()
    elif action == 'pause':
        client.pause()
    elif action == 'next':
        client.next()
    elif action == 'previous':
        client.previous()

    client.close()
    client.disconnect()
    
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
