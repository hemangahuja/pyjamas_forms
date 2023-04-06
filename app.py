from flask import Flask,request,render_template
import json
from database import Database
import crypto

form = json.load(open("form.json"))

print(form)
db = Database(form["db_name"] + ".csv")

app = Flask(__name__)


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html",form_name = form['form_name'], fields = form['form'].keys())
    

@app.route('/home')
def home():
    return render_template('home.html') 

@app.route("/submit",methods=["POST"])
def submit():
    row = {}
    print("request.form")
    print(request.form)
    for form_field,config in form["form"].items():
        data = request.form[form_field]
        if config['isEncrypted']:
            data = crypto.encrypt(data)
        row[form_field] = data
    # print(row)
    db.write(row)
    # db.show()
    
    return "submitted!"

@app.route("/find",methods=["POST"])
def find():
    try:
        # for key in request.form:
        #     if form['form'][key]:
        #         request.form[key] = crypto.encrypt(request.form[key])
        return db.find({key : {'data' : data,'isEncrypted' : form['form'][key]['isEncrypted']} for key,data in request.form.items()})
    except Exception as e:
        print("error",e)
        return "Not Found"

@app.route("/lookup",methods=["GET"])
def lookup():
    return render_template("lookup.html",form_name=form['form_name'],fields=[key for key,config in form['form'].items() if config['primaryKey']])