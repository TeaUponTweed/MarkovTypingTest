import itertools
import logging
import os
import pathlib
import pickle
import random

from flask import Flask, jsonify, send_file, send_from_directory
from markov_typing_test.markov import _gen_text

app = Flask(__name__)


@app.route("/")
def home():
    return send_file("static/index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


_MODEL = None
_FILE_DIR = pathlib.Path(__file__).parent.resolve()


@app.route("/text")
def text():
    global _MODEL
    if _MODEL is None:
        with open(os.path.join(_FILE_DIR, "model.pkl"), "rb") as fo:
            _MODEL = pickle.load(fo)
    words = list(itertools.islice(_gen_text(_MODEL), 300))

    return jsonify(
        {
            "words": words,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
