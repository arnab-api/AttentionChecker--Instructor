from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/post_gaze', methods=['POST']) 
def foo():
    data = request.json
    print(json.dumps(data, indent=2), type(data))
    # return jsonify({"response": "got some posted data!!!"})
    return jsonify(data)

if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'), 
        port=int(os.getenv('PORT', 5000)), 
        debug=True
    )
