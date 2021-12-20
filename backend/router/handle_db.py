from flask import Response, make_response, jsonify
from sqlalchemy import create_engine, Table, Column, MetaData, String, Integer
from sqlalchemy.sql import delete, update, insert, or_
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError
import os, hashlib, time


class Database:
    def createUser(self, form) -> Response:

        try:
            encryption = self.encryptPassword(password=form["password"]["password"])
            statement = insert(self.userAccounts).values(
                firstName=form["firstName"],
                lastName=form["lastName"],
                username=form["username"],
                email=form["email"],
                hash=encryption,
                gender=form["gender"],
                userCreated=int(time.time()),
                lastLogin=int(time.time()),
            )
            self.commitToDatabase(statement)
            return Response(status=200)

        except IntegrityError as e:
            return (
                self.createResponse("duplicate", "username", 200)
                if "username" in e.args[0]
                else self.createResponse("duplicate", "email", 200)
            )

        except Exception as e:
            print(e)
            return Response(status=500)

    def updateUser(self, form) -> Response:

        try:
            encryption = self.encryptPassword(password=form["password"]["password"])
            statement = update(self.userAccounts).values(
                firstName=form["firstName"],
                lastName=form["lastName"],
                username=form["username"],
                email=form["email"],
                gender=form["gender"],
                password_hash=encryption,
            )
            self.commitToDatabase(statement)
            return Response(status=200)

        except:
            return Response(status=500)

    def deleteUser(self, username) -> Response:

        try:
            statement = delete(self.userAccounts).where(
                self.userAccounts.c.username == username
            )
            self.commitToDatabase(statement)
            return Response(status=200)

        except:
            return Response(status=500)

    def authenticateUser(self, form) -> Response:

        try:
            storedHash = (
                Query(self.userAccounts.c.hash, session=self.session)
                .filter(
                    or_(
                        self.userAccounts.c.username == form["loginName"],
                        self.userAccounts.c.email == form["loginName"],
                    )
                )
                .first()
            )

            if not storedHash:
                return self.createResponse("loginError", "loginName", 200)

            storedSalt = storedHash[0][:32]
            newHash = self.encryptPassword(form["password"], storedSalt)

            if storedHash[0] != newHash:
                return self.createResponse("loginError", "password", 200)

            statement = update(self.userAccounts).values(lastLogin=int(time.time()))
            self.commitToDatabase(statement)

            return Response(status=200)

        except:
            return Response(status=500)

    def encryptPassword(self, password, salt=None) -> bytes:

        sha3 = hashlib.new("sha3_256")

        if not salt:
            randomSalt = os.urandom(32)
            sha3.update(randomSalt + bytes(password, "utf-8"))
            return randomSalt + sha3.digest()

        else:
            sha3.update(salt + bytes(password, "utf-8"))
            return salt + sha3.digest()

    def commitToDatabase(self, statement) -> None:
        self.session.execute(statement)
        self.session.commit()

    def createResponse(self, key, value, status) -> Response:

        response = make_response(jsonify({key: value}), status)
        return response

    engine = create_engine("sqlite:///backend/database/accounts.db")
    session = Session(engine)
    meta = MetaData()

    userAccounts = Table(
        "userAccounts",
        meta,
        Column("firstName", String),
        Column("lastName", String),
        Column("username", String, unique=True),
        Column("email", String, unique=True),
        Column("hash", String),
        Column("gender", String),
        Column("userCreated", Integer),
        Column("lastLogin", Integer),
    )
    # meta.create_all(engine)
