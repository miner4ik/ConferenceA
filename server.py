import time
from flask import Flask, request, Response

app = Flask(__name__)
messages = []
users = []


@app.route('/')
def index():
    return 'Hello'


@app.route("/status")
def status():
    return {
        'status': True,
        'time': time.time()

    }

@app.route("/history")
def history():
    """
        request: after
        response: {
            "messages": [
                {"username" : "str", "text":"str", "time": float},
                ...
            ]
        }
        """
    after = (float(request.args['after']))
    filtered_msg = []
    for message in messages:
        if after < message['time']:
            filtered_msg.append(message)
    return {"messages": filtered_msg}


@app.route("/send", methods=['POST'])
def send():
    data = request.json  # JSON -> dict
    username = data['username']
    text = data['text']
    messages.append({'username': username, 'text': text, 'time': time.time()})
    return Response(status=200)


app.run()
