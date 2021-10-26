from logging import debug
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user import User
from db import get_user


login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = "kamal"
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def home():
    # return "hello world"
    return render_template("index.html")


@app.route('/login', methods=['POST','GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)

        if user and user.change_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = "fail to login "
    return render_template('login.html', message=message)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


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

@login_manager.user_loader
def load_user(username):
    return get_user(username)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug= True)