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

db = firebase.database()



app = Flask(__name__)

model = pickle.load(open('cvd-model.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')


@app.route('/predict', methods=['POST'])
def predict():
    ints = [float(x) for x in request.form.values()]

    final = [np.array(ints)]
    prediction = model.predict(final)
    a = pd.Series(final).to_json(orient='values')
    output = model.predict_proba(final)
    if prediction==1:
        
        return render_template('report.html', pred = "Suffers from a CVD", prob = output )
    else:
        db.child("names").push({"age":request.form['age'], "gender":request.form['gender'], "chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope']})
        return render_template('report.html', pred= "Most Likely Healthy", prob = output )

    

if __name__ == '__main__':
    app.run(debug=True)