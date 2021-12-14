from flask import Response
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy.sql import select, delete, update, insert, or_
from sqlalchemy.orm import Session
from hashlib import pbkdf2_hmac
import os

class Database():

    def create_user(self, data) -> Response:

        try:
            encryption = self.encrypt_password(password=data["password"])
            statement = insert(self.user_accounts).values(
                first_name = data["first_name"],
                last_name = data["last_name"],
                username = data["username"],
                email = data["email"],
                hash = encryption
            )
            self.commit_to_database(statement)
            return Response(status=200)

        except:
            return Response(status=400)

    def update_user(self, data) -> Response:

        try:
            statement = update(self.user_accounts).values(
                first_name = data["first_name"],
                last_name = data["last_name"],
                username = data["username"],
                email = data["email"],
                password_hash = data["password"]
            )
            self.commit_to_database(statement)
            return Response(status=200)

        except:
            return Response(status=400)


    def delete_user(self, username) -> Response:

        try:
            statement = delete(self.user_accounts).where(
                self.user_accounts.c.username == username
            )
            self.commit_to_database(statement)
            return Response(status=200)

        except:
            return Response(status=400)


    def authenticate_user(self, credentials) -> Response:

        try:
            statement = select(self.user_accounts.c.hash).where(
                or_(
                    self.user_accounts.c.username==credentials["login_name"],
                    self.user_accounts.c.email==credentials["login_name"]
                )
            )
            stored_hash = self.session.execute(statement).one()[0]
            stored_salt = stored_hash[:32]
            new_hash = stored_salt + self.encrypt_password(credentials["password"], stored_salt)

            if stored_hash == new_hash:
                return Response(status=200)

            else:
                return Response(status=400)

        except:
            return Response(status=400)


    def encrypt_password(self, password, salt=None) -> Response:

        if salt:
            generated_hash = pbkdf2_hmac(
                "sha3_256",
                bytes(password, "utf-8"),
                salt,
                100_000,
                dklen=128
            )
            return generated_hash

        else:
            random_salt = os.urandom(32)

            generated_hash = pbkdf2_hmac(
                "sha3_256",
                bytes(password, "utf-8"),
                random_salt,
                100_000,
                dklen=128
            )
            return random_salt + generated_hash

    def commit_to_database(self, statement) -> None:
        self.session.execute(statement)
        self.session.commit()


    engine = create_engine("sqlite:///backend/database/accounts.db")
    session = Session(engine)
    meta = MetaData()

    user_accounts = Table(
        "user_accounts", meta,
        Column("username", String, primary_key=True, unique=True),
        Column("first_name", String),
        Column("last_name", String),
        Column("email", String, unique=True),
        Column("hash", String)
    )

