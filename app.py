import json
import logging
import logging.config

import crypto
from database import Database
from flask import Flask, render_template, request

'''
loading the config
'''
def load_form(filename: str = "C:\\Users\\Sreenath\\Desktop\\n1\\pyjamas_forms\\pyamas_config.json"):
    with open(filename, "r") as f:
        return json.load(f)


try:
    pyjamas_config = load_form()
except Exception as e:
    pyjamas_config = None

'''
create the database
'''
db = Database(pyjamas_config["db_name"] + ".csv") if pyjamas_config else None

app = Flask(__name__)

'''
    create a logger instance for logging purposes
'''
@app.before_first_request
def handle_logger():
    import os
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

'''
logging each request
'''
@app.before_request
def log_to_file():
    app.logger.debug("Request received: %s %s", request.method, request.url)

'''
load the configuration file and render the index template
'''
@app.route("/", methods=["GET"])
def index():
    try:
        pyjamas_config = load_form()
    except:
        pyjamas_config = None
    if pyjamas_config is not None:
        return render_template(
            "index.html",
            form_name=pyjamas_config["form_fields"],
            fields=pyjamas_config["form_fields"].keys(),
        )
    else:
        return render_template("index.html")

# @app.route("/home",methods=["GET"])
# def home():
#     return render_template("home.html")

'''
get a form response and encrypts the fields that are to be encrypted
writes the processed data to the database
'''
@app.route("/submit", methods=["POST"])
def submit():
    try:
        pyjamas_config = load_form()
    except:
        pyjamas_config = None
    row = {}
    print(request.form)
    for form_field, config in pyjamas_config["form_fields"].items():
        data = request.form[form_field]
        if config["isEncrypted"]:
            data = crypto.encrypt(data)
        row[form_field] = data
    db.write(row)

    return {"Submitted": True}

'''
gets a form response to be searched for in the database
decrypts the rows in database based on encryption key and matches to form response
returns the row if found
'''
@app.route("/find", methods=["POST"])
def find():
    try:
        pyjamas_config = load_form()
    except:
        pyjamas_config = None
    try:
        return db.find(
            {
                key: {
                    "data": data,
                    "isEncrypted": pyjamas_config["form_fields"][key]["isEncrypted"],
                }
                for key, data in request.form.items()
            },pyjamas_config
        )
    except Exception as e:
        print("error", e)
        return "Not Found"

'''
renders a ui for searching in the database with the appropriate primary keys
'''
@app.route("/lookup", methods=["GET"])
def lookup():
    try:
        pyjamas_config = load_form()
    except Exception as e:
        print(e)
        pyjamas_config = None
    return render_template(
        "lookup.html",
        form_name=pyjamas_config["form_name"],
        fields=[
            key
            for key, config in pyjamas_config["form_fields"].items()
            if config["primaryKey"]
        ],
    )

'''
renders a ui for inserting a row in database
'''
@app.route("/insert",methods=["GET"])
def insert():
    try:
        pyjamas_config = load_form()
    except Exception as e:
        print(e)
        pyjamas_config = None
    return render_template(
        "submit.html",
        form_name=pyjamas_config["form_name"],
        fields=
            list(dict(pyjamas_config["form_fields"].items()).keys())
        ,
    )

'''
runs the application
'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
