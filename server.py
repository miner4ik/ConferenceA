import time
from flask import Flask, request, Response

app = Flask(__name__)
all_data = {'global': []}


@app.route('/')
def index():
    return 'Hello'

@app.route("/status")
def status():
    return {
        'status': True,
        'time': time.time()

    }


@app.route("/history/<group>")
def history(group):
    """
        request: after
        response: {
            "messages": [
                {"username" : "str", "text":"str", "time": float},
                ...
            ]
        }
        """
    try:
        all_data[group]
    except KeyError:
        all_data[group] = []

    messages = all_data[group]
    after = (float(request.args['after']))
    filtered_msg = []
    for message in messages:
        if after < message['time']:
            filtered_msg.append(message)
    return {"messages": filtered_msg}


@app.route("/send/<group>", methods=['POST'])
def send(group):
    data = request.json  # JSON -> dict
    username = data['username']
    text = data['text']
    try:
        all_data[group]
    except KeyError:
        all_data[group] = []
    messages = all_data[group]
    messages.append({'username': username, 'text': text, 'time': time.time()})

    return Response(status=200)



app.run()
