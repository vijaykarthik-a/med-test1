# api.py
import eventlet
eventlet.monkey_patch()
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import json

# --- Basic Setup ---
app = Flask(__name__)
# Allow cross-origin requests, which is necessary for your GitHub Pages frontend
CORS(app, resources={r"/*": {"origins": "*"}}) 
# Use eventlet as the async server for WebSocket performance
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

DATA_FILE = "data.json"

# --- Helper Function ---
def get_data_from_file():
    """Reads the current data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a default structure if the file doesn't exist or is empty
        return {"error": "Data file not found or is invalid."}

# --- WebSocket Event Handlers ---
@socketio.on('connect')
def handle_connect():
    """
    This function is triggered when a new user opens your dashboard.
    It sends them the most current data right away.
    """
    print(f"✅ Client connected: {request.sid}")
    initial_data = get_data_from_file()
    # 'emit' sends an event and data to the connected client
    socketio.emit('update_data', initial_data, room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print(f"❌ Client disconnected: {request.sid}")

# --- API Routes ---
@app.route('/api/trigger-update', methods=['POST'])
def trigger_update():
    """
    This is a special, hidden endpoint. 
    Our scheduled script will call this to tell the server it's time to update everyone.
    """
    print("🔄 Update triggered by scheduled task! Broadcasting new data...")
    latest_data = get_data_from_file()
    # Broadcast the 'update_data' event to ALL connected clients
    socketio.emit('update_data', latest_data)
    return jsonify({"status": "success", "message": "Update broadcasted to all clients."})

# --- Main Entry Point ---
if __name__ == '__main__':
    print("🚀 Starting Flask-SocketIO server...")
    # Use socketio.run() to correctly start the WebSocket server
    socketio.run(app, debug=True, port=5000)
