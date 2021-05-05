#!/usr/bin/env python3
from flask import Flask, request, jsonify, redirect, make_response
from sqlitedict import SqliteDict
from functools import wraps
import random
import string

app = Flask(__name__)

def corsify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        value = f(*args, **kwargs)
        resp = make_response(value)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    return wrapper



@app.route("/")
@corsify
def create_url():
    if not request.args.get("url"):
        return "please specify a url query parameter to redirect and try again", 400

    charset = string.ascii_letters + string.digits
    randomised_url = "".join([charset[random.randrange(len(charset))] for i in range(9)])

    with SqliteDict("./data.db") as dbs:
       dbs[randomised_url] = request.args.get("url") 
       dbs.commit()

    return jsonify(dict(short_path=randomised_url))

@app.route("/<short_path>")
@corsify
def route(short_path):
    with SqliteDict("./data.db") as dbs:
        url = dbs.get(short_path)

        if url is None:
            return "Please recheck the URL and try again !", 400

    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True)
