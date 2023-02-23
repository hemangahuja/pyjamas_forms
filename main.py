from flask import Flask,request,render_template
import json
from database import Database
import crypto

form = json.load(open("form.json"))

print(form)

app = Flask(__name__)


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html",form_name = form['form_name'], fields = form['form'].keys())
    


@app.route("/submit",methods=["POST"])
def submit():
    db = Database(form["db_name"] + ".csv")
    row = {}
    print("request.form")
    print(request.form)
    for form_field,isEncrypted in form["form"].items():
        data = request.form[form_field]
        if isEncrypted:
            data = crypto.encrypt(data)

        row[form_field] = data
    print(row)
    db.write(row)
    
    return "submitted!"
