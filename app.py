from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Hello from Kubernetes on Windows! Host: {os.environ.get('HOSTNAME', 'Unknown')}"

@app.route('/health')
def health():
    return 'Healthy', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)