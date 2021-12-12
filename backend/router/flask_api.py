import handle_db
from flask import Flask, Response, request
from flask_cors import CORS #, cross_origin

app = Flask(__name__)
Cors = CORS(app)

@app.route("/api/v1/login", methods=["POST"])
def login_user() -> Response:

    credentials = request.get_json()
    response = database.authenticate_user(credentials)

    return response


@app.route("/api/v1/register", methods=["POST"])
def register_user() -> Response:
    
    data = request.get_json()
    response = database.create_user(data)

    return response

@app.route("/api/v1/delete", methods=["POST"])
def delete_user() -> Response:

    data = request.get_json()
    response = database.delete_user(data)

    return response

# @app.route("/api/create_user", methods=["POST"])
# def create_account():

#     data = request.get_json()
#     password_hash = handle_db.hash_password(data["password"])
    
#     response = handle_db.create_user(
#         data["first_name"],
#         data["last_name"],
#         data["username"],
#         data["email"],
#         password_hash
#     )

#     return response


if __name__ == "__main__":
    database = handle_db.Database()
    app.run()
