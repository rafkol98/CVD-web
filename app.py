from flask import Flask, render_template, request, redirect, url_for, jsonify, after_this_request
import lime
import pdfkit
from dataset import firstGraph, secondGraph, getVar, countVar, getNumberPatientsMore, getNumberPatientsLess
from lime import lime_tabular
import pickle
import datetime
import numpy as np
import pandas as pd
import pyrebase
import dill
import json
# import dataset

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

app = Flask(__name__)
# Load model.
model = pickle.load(open('cvd-model.pkl','rb'))
with open("explainer.pkl", 'rb') as f: exp_load = dill.load(f)

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

            prob_neg = str(model.predict_proba(final)[:,0])[1:-1]
            prob_pos = str(model.predict_proba(final)[:,1])[1:-1]
        
            if prediction==1:
                db.child(uid).child("Patients").child(pid).child("latest").set({"cardio":1})
                db.child(uid).child("Patients").child(pid).child("current").update({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":1})
                db.child(uid).child("Patients").child(pid).child("history").child(ct).set({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":1})
                return redirect(url_for('report', pred = "Suffers from a CVD", neg = prob_neg, pos = prob_pos, pid = pid, uid = uid ))
            else:
                db.child(uid).child("Patients").child(pid).child("latest").set({"latest":0})
                db.child(uid).child("Patients").child(pid).child("current").update({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":0})
                db.child(uid).child("Patients").child(pid).child("history").child(ct).set({"chest":request.form['chest'], "bps":request.form['bps'], "chol":request.form['chol'], "fbs":request.form['fbs'], "ecg":request.form['ecg'], "maxheart":request.form['maxheart'], "exang":request.form['exang'], "oldpeak":request.form['oldpeak'], "stslope":request.form['stslope'], "cardio":0})
                return redirect(url_for('report', pred= "Most Likely Healthy", neg = prob_neg, pos = prob_pos, pid = pid, uid = uid ))
    else:
        pid = request.args.get('pid')
        return render_template('diagnose.html', pid = pid)

@app.route('/patients/', methods=['GET','POST'])
def patients():
        if request.method == 'POST':
        # Get uid of user logged in.
            uid = request.form['user_id']

            patient_data = {"age":request.form['age'], "gender":request.form['gender'], "name":request.form['name'], "lastName":request.form['lastName'], "email":request.form['email']}
            db.child(uid).child("Patients").push(patient_data)
            
            return redirect(url_for('patients'))
        else:
            return render_template('patients.html')

# Generate visual report.
@app.route('/report')
def report():
    pred = request.args.get('pred')
    neg = request.args.get('neg')
    pos = request.args.get('pos')
    uid = request.args.get('uid')
    pid = request.args.get('pid')

    # Get patient.
    patient = db.child(uid).child("Patients").child(pid).get()
    # Get current diagnosis data.
    diagnosisData = db.child(uid).child("Patients").child(pid).child("current").get()

    # Make an array with all the patient's data.
    data = (np.array([patient.val()['age'], patient.val()['gender'], diagnosisData.val()['chest'], diagnosisData.val()['bps'], diagnosisData.val()['chol'], diagnosisData.val()['fbs'], diagnosisData.val()['ecg'], diagnosisData.val()['maxheart'], diagnosisData.val()['exang'], diagnosisData.val()['oldpeak'], diagnosisData.val()['stslope']])).astype(float)
    
    # Make the first graph.
    graphOne = [ diagnosisData.val()['chest'], diagnosisData.val()['fbs'], diagnosisData.val()['ecg'], diagnosisData.val()['exang'], diagnosisData.val()['oldpeak'], diagnosisData.val()['stslope'] ]

    graphTwo = [ diagnosisData.val()['bps'], diagnosisData.val()['chol'], diagnosisData.val()['maxheart'] ]

    # Explainable AI.
    exp = exp_load.explain_instance(data_row = data, predict_fn = model.predict_proba)
    exp = exp.as_html()

    healthyAvg = firstGraph(0)
    cardioAvg = firstGraph(1)

    healthySecAvg = secondGraph(0)
    cardioSecAvg = secondGraph(1)

    healthyAge = getVar("age", 0)
    cardioAge = getVar("age", 1)

    healthyGender = getVar("sex", 0)
    cardioGender = getVar("sex", 1)

    healthyChol = getVar("cholesterol", 0)
    cardioChol = getVar("cholesterol", 1)
    
    # Get number of healthy patients more than patient's value.
    numMoreHealthyChol = getNumberPatientsMore("cholesterol", diagnosisData.val()['chol'], 0)
    numLessHealthyChol = getNumberPatientsLess("cholesterol", diagnosisData.val()['chol'], 0)
    healthyCholMoreLess = [numLessHealthyChol, numMoreHealthyChol]

    # Get number of cardio patients more than patient's value.
    numMoreCardioChol = getNumberPatientsMore("cholesterol", diagnosisData.val()['chol'], 1)
    numLessCardioChol = getNumberPatientsLess("cholesterol", diagnosisData.val()['chol'], 1)
    cardioCholMoreLess = [numLessCardioChol, numMoreCardioChol]

    # Get number of healthy patients more than patient's value.
    numMoreHealthyRBP = getNumberPatientsMore("resting bp s", diagnosisData.val()['bps'], 0)
    numLessHealthyRBP = getNumberPatientsLess("resting bp s", diagnosisData.val()['bps'], 0)
    healthyRBPMoreLess = [numLessHealthyRBP, numMoreHealthyRBP]

    # Get number of cardio patients more than patient's value.
    numMoreCardioRBP = getNumberPatientsMore("resting bp s", diagnosisData.val()['bps'], 1)
    numLessCardioRBP = getNumberPatientsLess("resting bp s", diagnosisData.val()['bps'], 1)
    cardioRBPMoreLess = [numLessCardioRBP, numMoreCardioRBP]

    # Get number of healthy patients more than patient's value.
    numMoreHealthyMaxHeart = getNumberPatientsMore("max heart rate", diagnosisData.val()['maxheart'], 0)
    numLessHealthyMaxHeart = getNumberPatientsLess("max heart rate", diagnosisData.val()['maxheart'], 0)
    healthyMaxHeartMoreLess = [numLessHealthyMaxHeart, numMoreHealthyMaxHeart]

    # Get number of cardio patients more than patient's value.
    numMoreCardioMaxHeart = getNumberPatientsMore("max heart rate", diagnosisData.val()['maxheart'], 1)
    numLessCardioMaxHeart = getNumberPatientsLess("max heart rate", diagnosisData.val()['maxheart'], 1)
    cardioMaxHeartMoreLess = [numLessCardioMaxHeart, numMoreCardioMaxHeart]

    healthyRBP = getVar("resting bp s", 0)
    cardioRBP = getVar("resting bp s", 1)

    healthyHeart = getVar("max heart rate", 0)
    cardioHeart = getVar("max heart rate", 1)

    healthyChest = getVar("chest pain type", 0)
    cardioChest = getVar("chest pain type", 1)

    healthyOldpeak = getVar("oldpeak", 0)
    cardioOldpeak = getVar("oldpeak", 1)

    healthyECG = getVar("resting ecg", 0)
    cardioECG = getVar("resting ecg", 1)

    healthyStSlope = getVar("ST slope", 0)
    cardioStSlope = getVar("ST slope", 1)

#   Count fbs 0 and 1 in healthy and cardio patients.
    countHealFBS_0 = countVar("fasting blood sugar",0,0)
    countHealFBS_1 = countVar("fasting blood sugar",0,1)

    countCardioFBS_0 = countVar("fasting blood sugar",1,0)
    countCardioFBS_1 = countVar("fasting blood sugar",1,1)

    healthyFBS = [countHealFBS_0, countHealFBS_1]
    cardioFBS = [countCardioFBS_0, countCardioFBS_1]

#   Count exercise angina 0 and 1 in healthy and cardio patients.
    healthyExang = [countVar("exercise angina",0,0), countVar("exercise angina",0,1)]
    cardioExang = [countVar("exercise angina",1,0), countVar("exercise angina",1,1)]

    return render_template('report.html', pred = pred, neg = neg, exp = exp, pos = pos, pid = pid, data = data, graphOne = graphOne, healthyChol = healthyChol, healthyAge = healthyAge, cardioChol = cardioChol, cardioAge = cardioAge, rbp = diagnosisData.val()['bps'], sex = patient.val()['gender'], age = patient.val()['age'], chol = diagnosisData.val()['chol'], maxHeart = diagnosisData.val()['maxheart'], chest = diagnosisData.val()['chest'], fbs = diagnosisData.val()['fbs'], oldpeak = diagnosisData.val()['oldpeak'], exang = diagnosisData.val()['exang'], stslope = diagnosisData.val()['stslope'], ecg = diagnosisData.val()['ecg'], healthyAvg = healthyAvg, cardioAvg = cardioAvg, healthySecAvg = healthySecAvg, cardioSecAvg = cardioSecAvg, graphTwo = graphTwo, healthyRBP = healthyRBP, cardioRBP = cardioRBP, healthyHeart = healthyHeart, cardioHeart = cardioHeart, healthyChest = healthyChest, cardioChest = cardioChest, countHealFBS_0 = countHealFBS_0, countHealFBS_1 = countHealFBS_1, countCardioFBS_0 = countCardioFBS_0, countCardioFBS_1 = countCardioFBS_1, healthyFBS = healthyFBS, cardioFBS = cardioFBS, healthyOldpeak = healthyOldpeak, cardioOldpeak = cardioOldpeak, healthyExang = healthyExang, cardioExang = cardioExang, healthyStSlope = healthyStSlope, cardioStSlope = cardioStSlope, healthyECG = healthyECG, cardioECG = cardioECG, healthyGender = healthyGender, cardioGender = cardioGender, healthyCholMoreLess = healthyCholMoreLess, cardioCholMoreLess = cardioCholMoreLess, healthyRBPMoreLess = healthyRBPMoreLess, cardioRBPMoreLess = cardioRBPMoreLess, healthyMaxHeartMoreLess = healthyMaxHeartMoreLess, cardioMaxHeartMoreLess = cardioMaxHeartMoreLess)


# Get patients of user.
@app.route('/getPatients', methods=['GET'])
def getPatients():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    uid = request.args.get('uid')

    patients = db.child(uid).child("Patients").get().val()

    return jsonify(patients)


# Get a patient's info.
@app.route('/patients/info', methods=['GET'])
def info():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    uid = request.args.get('uid')
    pid = request.args.get('pid')

    patient = db.child(uid).child("Patients").child(pid).get()

    jsonResp = {'name': patient.val()['name'],'age': patient.val()['age'], 'gender': patient.val()['gender'], 'email': patient.val()['email']}
    return jsonify(jsonResp)


# Get a patient's history.
@app.route('/patients/history', methods=['GET'])
def history():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    uid = request.args.get('uid')
    pid = request.args.get('pid')

    history = db.child(uid).child("Patients").child(pid).child("history").get().val()

    return jsonify(history)


@app.route('/edit/', methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        uid = request.args.get('uid')
        pid = request.args.get('pid')

        patient_data = {"age":request.form['age'], "gender":request.form['gender'], "name":request.form['name'], "lastName":request.form['lastName'], "email":request.form['email']}
        db.child(uid).child("Patients").child(pid).update(patient_data)

        return redirect(url_for('edit', uid = uid, pid = pid, update="Patient data was successfully updated!"))

    else:
        uid = request.args.get('uid')
        pid = request.args.get('pid')
       
        # if uid and pid are not None, then return edit form for patient.
        if uid is not None and pid is not None:
            patient = db.child(uid).child("Patients").child(pid).get()

            name = patient.val()['name']
            lastName = patient.val()['lastName']
            email = patient.val()['email']
            gender = patient.val()['gender']
            age =  patient.val()['age']

            return render_template('edit.html', uid = uid, pid = pid, name = name, lastName = lastName, email = email, gender = gender, age = age)
        else:
            return render_template('patients.html')

@app.route('/delete/')
def delete():
    
    uid = request.args.get('uid')
    pid = request.args.get('pid')

    db.child(uid).child("Patients").child(pid).remove()

    return render_template('patients.html', update="Patient was deleted successfully." )



if __name__ == '__main__':
    app.run(debug=True)