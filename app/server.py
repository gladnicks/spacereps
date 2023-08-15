import json

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/decks", methods=["GET"])
def load_decks():
    try:
        with open("decks.json", "r") as decks_file:
            decks = json.load(decks_file)
    except FileNotFoundError:
        with open("decks.json", "w") as new_decks_file:
            decks = {"decks": []}
            json.dump(decks, new_decks_file, indent=4)
    
    resp = jsonify(decks)
    return resp

if __name__ == "__main__":
    app.run("localhost", 9876, debug=True)