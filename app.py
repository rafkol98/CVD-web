from flask import Flask, render_template, request, redirect, url_for, jsonify, after_this_request
import pickle
import datetime
import numpy as np
import pandas as pd
import pyrebase

config = {
    "apiKey": "AIzaSyB6qq3TuV541bSWJzmnOgHm1F90a7sH0yE",
    "authDomain": "cardio-82209.firebaseapp.com",
    "databaseURL": "https://cardio-82209-default-rtdb.firebaseio.com",
    "projectId": "cardio-82209",
    "storageBucket": "cardio-82209.appspot.com",
    "messagingSenderId": "792713522509",
    "appId": "1:792713522509:web:859deb8956aee32fa01b04",
    "measurementId": "G-H0RD6F6TJQ"
  }

firebase = pyrebase.initialize_app(config)

# Get firebase database.
db = firebase.database()

# user = db.child(firebase.currentUser().uid)

app = Flask(__name__)
# Load model.
model = pickle.load(open('cvd-model.pkl','rb'))

# Get patients
def getPatients(u_id):
    return db.child(u_id).child("Patients").get().val()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose/', methods=['GET','POST'])
def diagnose():
    if request.method == 'POST':

        # Get uid of user logged in.
        uid = request.form['user_id']

        # Get patient id.
        pid = request.args.get('pid')

        age = db.child(uid).child("Patients").child(pid).child("age").get().val()

        gender = db.child(uid).child("Patients").child(pid).child("gender").get().val()

        if((age is not None) and (gender is not None)):

            # Get all the values from the form.
            ints = [age, gender, request.form['chest'],request.form['bps'], request.form['chol'],request.form['fbs'],request.form['ecg'], request.form['maxheart'], request.form['exang'], request.form['oldpeak'], request.form['stslope']]
            # TODO - ERROR CHECKING.

        
            # Get current timestamp.
            ct = int(datetime.datetime.now().timestamp())
        

            final = [np.array(ints)]
            prediction = model.predict(final)
            a = pd.Series(final).to_json(orient='values')
            output = model.predict_proba(final)

            if prediction==1:
                db.child(uid).child("Patients").child(pid).child("latest").update({"cardio":1})
                db.child(uid).child("Patients").child(pid).child("current").update({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":1})
                db.child(uid).child("Patients").child(pid).child("history").child(ct).set({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":1})
                return redirect(url_for('report', pred = "Suffers from a CVD", prob = output, pid = pid, uid = uid ))
            else:
                db.child(uid).child("Patients").child(pid).update({"latest":0})
                db.child(uid).child("Patients").child(pid).child("current").update({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":0})
                db.child(uid).child("Patients").child(pid).child("history").child(ct).set({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":0})
                return redirect(url_for('report', pred= "Most Likely Healthy", prob = output, pid = pid, uid = uid ))
    else:
        pid = request.args.get('pid')
        return render_template('diagnose.html', pid = pid)


@app.route('/patients/', methods=['GET','POST'])
def patients():
        if request.method == 'POST':
        # Get uid of user logged in.
            uid = request.form['user_id']

            db.child(uid).child("Patients").push({"age":request.form['age'], "gender":request.form['gender'], "name":request.form['name'], "email":request.form['email']})
            return redirect(url_for('patients'))
        else:
            return render_template('patients.html')

@app.route('/report')
def report():
    pred = request.args.get('pred')
    prob = request.args.get('prob')
    uid = request.args.get('uid')
    pid = request.args.get('pid')

    diagnosisData = db.child(uid).child("Patients").child(pid).child("current").get()

    data = [ diagnosisData.val()['bps'], diagnosisData.val()['chol'], diagnosisData.val()['maxheart'] ]
    return render_template('report.html', pred = pred, prob = prob, pid = pid, data = data)


@app.route('/patients/hello', methods=['GET'])
def hello():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    uid = request.args.get('uid')
    pid = request.args.get('pid')

    patient = db.child(uid).child("Patients").child(pid).get()

    jsonResp = {'age': patient.val()['age'], 'gender': patient.val()['gender'], 'email': patient.val()['email']}
    return jsonify(jsonResp)


if __name__ == '__main__':
    app.run(debug=True)