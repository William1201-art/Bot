from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return "Discord Bot Server is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "service": "discord-bot"}

def server_on():
    """Start the Flask server in a separate thread to keep the Discord bot alive"""
    def run():
        app.run(host='0.0.0.0', port=5000, debug=False)
    
    server_thread = threading.Thread(target=run)
    server_thread.daemon = True
    server_thread.start()
    print("🌐 Flask server started on http://0.0.0.0:5000")