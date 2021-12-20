from flask.helpers import make_response
import handle_db
from flask import Flask, Response, request
from flask_cors import CORS #, cross_origin

app = Flask(__name__)
Cors = CORS(app)

@app.route("/api/v1/login", methods=["POST"])
def loginUser() -> Response:

    form = request.get_json()
    response = database.authenticateUser(form)

    return response


@app.route("/api/v1/register", methods=["POST"])
def registerUser() -> Response:
    
    form = request.get_json()
    response = database.createUser(form)

    return response

@app.route("/api/v1/delete", methods=["POST"])
def deleteUser() -> Response:

    form = request.get_json()
    response = database.deleteUser(form)

    return response


if __name__ == "__main__":
    database = handle_db.Database()
    app.run()
