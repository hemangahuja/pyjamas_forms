import json
import logging
import logging.config

import crypto
from database import Database
from flask import Flask, render_template, request


def load_form(filename: str = "pyjamas_config.json"):
    with open(filename, "r"):
        return json.load(open("pyjamas_config.json"))


pyjamas_config = load_form()

db = Database(pyjamas_config["db_name"] + ".csv")

app = Flask(__name__)


@app.before_request
def log_request():
    app.logger.debug("Request received: %s %s", request.method, request.url)


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        form_name=pyjamas_config["form_fields"],
        fields=pyjamas_config["form_fields"].keys(),
    )


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/submit", methods=["POST"])
def submit():
    row = {}
    print(request.form)
    for form_field, config in pyjamas_config["form_fields"].items():
        data = request.form[form_field]
        if config["isEncrypted"]:
            data = crypto.encrypt(data)
        row[form_field] = data
    # print(row)
    db.write(row)
    # db.show()

    return {"Submitted": True}


@app.route("/find", methods=["POST"])
def find():
    try:
        return db.find(
            {
                key: {
                    "data": data,
                    "isEncrypted": pyjamas_config["form_fields"][key]["isEncrypted"],
                }
                for key, data in request.form.items()
            }
        )
    except Exception as e:
        print("error", e)
        return "Not Found"


@app.route("/lookup", methods=["GET"])
def lookup():
    return render_template(
        "lookup.html",
        form_name=pyjamas_config["form_name"],
        fields=[
            key
            for key, config in pyjamas_config["form_fields"].items()
            if config["primaryKey"]
        ],
    )


if __name__ == "__main__":
    import logging

    logging.basicConfig(filename="error.log", level=logging.DEBUG)
    app.run(host="0.0.0.0", port=80, debug=True)
