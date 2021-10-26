from logging import debug
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    # return "hello world"
    return render_template("index.html")

@app.route("/chat")
def chat():
    username = request.args.get("username")
    room = request.args.get("room")
    
    if username and room:
        return render_template("chat.html", username = username, room = room)
    else:
        return redirect(url_for("home"))


@socketio.on("send_message")
def handle_send_message(data):
    app.logger.info("{} has send the message to room {}: {}".format(data['username'],data['room'], data['message']))

    socketio.emit('receive_message', data, room=data['room'])

@socketio.on("join_room")
def handle_join_room_event(data):
    print("data---->",data)
    app.logger.info("{} has joined the room {}".format(data['username'], data["room"]) )
    join_room(data['room'])
    socketio.emit("join_room_announcement",data)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug= True)