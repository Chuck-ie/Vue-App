from flask import Flask, request, jsonify
from flask_cors import CORS#, cross_origin

app = Flask(__name__)
Cors = CORS(app)

@app.route("/api/login", methods=["POST", "GET"])
def handle_login():
    
    if request.method == "POST":
        data = request.get_json()
        return jsonify({
            "username": data["username"],
            "password": data["password"]
        })

    elif request.method == "GET":
        return jsonify("Get Request!")

    else:
        return jsonify("HELLO!")


@app.route("/")
def hello():
    return jsonify("Hello")

if __name__ == "__main__":
    app.run()
