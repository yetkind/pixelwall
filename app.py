from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet


app = Flask(__name__)
socketio = SocketIO(app)


canvas_width = 100  
canvas_height = 100  
canvas = [[None for _ in range(canvas_width)] for _ in range(canvas_height)]  


connected_users = 0

@app.route('/')
def index():
    return render_template('index.html', width=canvas_width, height=canvas_height)

@socketio.on('connect')
def handle_connect():
    global connected_users
    connected_users += 1
    emit('update_user_count', connected_users, broadcast=True)
    print(f"A user connected. Total: {connected_users}")

@socketio.on('disconnect')
def handle_disconnect():
    global connected_users
    connected_users -= 1
    emit('update_user_count', connected_users, broadcast=True)
    print(f"A user disconnected. Total: {connected_users}")

@socketio.on('place_pixel')
def handle_place_pixel(data):
    x = data['x']
    y = data['y']
    color = data['color']

    
    canvas[y][x] = color

    
    emit('pixel_update', {'x': x, 'y': y, 'color': color}, broadcast=True)

@socketio.on('get_canvas')
def handle_get_canvas():

    emit('canvas_state', canvas)

if __name__ == '__main__':
    socketio.run(app, debug=True)
