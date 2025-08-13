from flask import Flask
import os  # Add this import for dynamic port

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! I am running on Python in OpenShift!\n'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080)) 
    app.run(host='0.0.0.0', port=port)
