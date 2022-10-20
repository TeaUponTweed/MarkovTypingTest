import logging
import os
import pathlib
import random

from flask import Flask, jsonify, send_file, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return send_file("static/index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/text")
def text():
    return jsonify(
        {
            "words": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.".split(),
            # "words": "zoop zoop".split(),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
