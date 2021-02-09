from flask import Flask, render_template, request
import pickle
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose/<patient_id>')
def diagnose(patient_id):
    return render_template('diagnose.html')

@app.route('/addpatient', methods=['POST'])
def addpatient():
     if request.method == 'POST':
        # Get uid of user logged in.
        uid = request.form['uid']

        db.child(uid).child("Patients").push({"age":request.form['age'], "gender":request.form['gender'], "name":request.form['name'], "email":request.form['email']})
        return render_template('patients.html')

@app.route('/patients/<u_id>')
def patients(u_id):
    
    x = db.child(u_id).child("Patients").child("-MT1IE-trJTZLMuEoMGT").get().val()
    return render_template('patients.html', x=x)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get all the values from the form.
        ints = [request.form['age'], request.form['gender'], request.form['chest'],request.form['bps'], request.form['chol'],request.form['fbs'],request.form['ecg'], request.form['maxheart'], request.form['exang'], request.form['oldpeak'], request.form['stslope']]
        # TODO - ERROR CHECKING.
        
        # Get uid of user logged in.
        uid = request.form['uid']

        final = [np.array(ints)]
        prediction = model.predict(final)
        a = pd.Series(final).to_json(orient='values')
        output = model.predict_proba(final)

        if prediction==1:
            db.child(uid).child("Patients").child("patientid").child("history").child("timestamp").push({"age":request.form['age'], "gender":request.form['gender'], "chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":1})
            return render_template('report.html', pred = "Suffers from a CVD", prob = output )
        else:
            db.child(uid).child("Patients").child("patientid").child("history").child("timestamp").push({"age":request.form['age'], "gender":request.form['gender'], "chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":0})
            return render_template('report.html', pred= "Most Likely Healthy", prob = output )
    

if __name__ == '__main__':
    app.run(debug=True)