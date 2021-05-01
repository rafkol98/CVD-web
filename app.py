from flask import Flask, render_template, request, redirect, url_for, jsonify, after_this_request, abort, flash, session
import sentry_sdk
from flask import Flask
from datetime import timedelta
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_mail import Mail, Message
from dataset import firstGraph, secondGraph, getVar, countVar, getNumberPatientsMore, getNumberPatientsLess
import pickle
import datetime
import numpy as np
import pandas as pd
import pyrebase
import dill
import json
import re
import os


app = Flask(__name__)

# Sentry.io setup.
sentry_sdk.init(
    dsn="https://1b6924d4293e46e286182d21cbbca7d5@o577693.ingest.sentry.io/5733223",
    integrations=[FlaskIntegration()],

    traces_sample_rate=1.0
)

# Firebase
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

# Firebase initialisation
firebase = pyrebase.initialize_app(config)

# Logout user automatically after 5 days.
app.permanent_session_lifetime = timedelta(days=5)

# Initialisation of Firebase authentication.
auth = firebase.auth()

# Initialisation of Firebase database
db = firebase.database()

# Initialisation of Firebase storage
storage = firebase.storage()

app.secret_key = "OMONOIALAOSPROTATHLIMA"


@app.before_request
def func():
  session.modified = True

# Load model.
model = pickle.load(open('random_forest.pkl','rb'))
with open("explainer_lime.pkl", 'rb') as f: exp_load = dill.load(f)

# Get number of more and less of the condition and variable passed in.
def getNumbers(name, variable, condition):
    numMore = getNumberPatientsMore(name, variable, condition)
    numLess = getNumberPatientsLess(name, variable, condition)
    return [numMore, numLess]

# Check a number is within the limits.
def check_number(string, min, max):
    if string.isdecimal():
        numeric = int(string)
        return min <= numeric <= max
    else:
        return False 

# Check if string contains only letters.
def only_letters(string):
    return all(letter.isalpha() for letter in string)

# Check if string contains only letters.
def check_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    return re.search(regex, email)

# Get id of last child in the list.
def getLastId(list):
    return list[-1]

# Save to database.
def save_to_db(ct, uid, pid, chest, bps, chol, fbs, ecg, maxheart, exang, oldpeak, stslope, outcome):
    db.child(uid).child("Patients").child(pid).update({"latest":outcome})
    db.child(uid).child("Patients").child(pid).child("current").update({"chest":chest, "bps":bps, "chol":chol, "fbs":fbs, "ecg":ecg, "maxheart":maxheart, "exang":exang, "oldpeak":oldpeak, "stslope":stslope, "cardio":outcome})
    db.child(uid).child("Patients").child(pid).child("history").child(ct).set({"chest":chest, "bps":bps, "chol":chol, "fbs":fbs, "ecg":ecg, "maxheart":maxheart, "exang":exang, "oldpeak":oldpeak, "stslope":stslope, "cardio":outcome})

# Not found error.
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Server error.
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")

# Forbidden error.
@app.errorhandler(403)
def forbidden_error(e):
    return render_template("403.html")

# Main functions
@app.route('/')
def index():
    try:
        print(session['usr'])
        return redirect(url_for('patients'))
    except:
        return render_template('index.html')

# Logout user.
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Signup user.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        rep_password = request.form["rep_password"]
        
        # Check if passwords match and check email.
        if (password == rep_password) and check_email(email):
            try:
                # create user.
                auth.create_user_with_email_and_password(email, password)
            except:
                flash("User already exists.", "danger")
                return redirect(url_for('signup'))
            # 
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = auth.current_user['localId']
            session['usr'] = user_id
            return redirect(url_for('patients'))
        else:
            flash("Please ensure passwords match and email is valid.", "danger")
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html') 
    

# Login user
@app.route('/login', methods=['POST'])
def login():
    try:
        print(session['usr'])
        return redirect(url_for('patients'))
    except KeyError:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user_id = auth.current_user['localId']
                session['usr'] = user_id

                return redirect(url_for('patients'))
            except:
                flash("Couldn't sign in, ensure email and password are correct.", "danger")
                return redirect(url_for('index'))


# Load no login page.
@app.route('/no_login', methods=['GET','POST'])
def no_login():
    if request.method == 'POST':
        # Get data passed in the form.
        age = request.form['age']
        gender = request.form['gender']
        chest = request.form['chest']
        bps = request.form['bps']
        chol = request.form['chol'] 
        fbs = request.form['fbs']
        ecg = request.form['ecg']
        maxheart = request.form['maxheart']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        stslope = request.form['stslope']

        # Put the data in an array.
        ints = [age, gender, chest, bps, chol, fbs, ecg, maxheart, exang, oldpeak, stslope]
        
        # Error checking for the passed in data.
        if all(ints) and check_number(bps, 0, 300) and check_number(chol, 0, 700) and check_number(maxheart, 0, 300) and (0 <= float(oldpeak) <= 7) and check_number(chest, 1, 4) and check_number(fbs, 0, 1) and check_number(ecg, 0, 2) and check_number(exang, 0, 1) and check_number(stslope, 0, 3):
            # Generate report.

            final = [np.array(ints)]

            # Get data in an appropriate form.
            data = (np.array(ints)).astype(float)

            pred = ''

            if model.predict(final) == 0:
                pred = "Most Likely Healthy"
            else:
                pred = "Most Likely CVD"
            
            neg = str(model.predict_proba(final)[:,0])[1:-1]
            pos = str(model.predict_proba(final)[:,1])[1:-1]

            # Make the first graph.
            graphOne = [ chest, fbs, ecg, exang, oldpeak, stslope ]

            graphTwo = [ bps, chol, maxheart ]

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
            healthyCholMoreLess = getNumbers("cholesterol", chol, 0)

            # Get number of cardio patients more than patient's value.
            cardioCholMoreLess = getNumbers("cholesterol", chol, 1)

            # Get number of healthy patients more than patient's value.
            healthyRBPMoreLess = getNumbers("resting bp s", bps, 0)

            # Get number of cardio patients more than patient's value.
            cardioRBPMoreLess = getNumbers("resting bp s", bps, 1)

            # Get number of healthy patients more than patient's value.
            healthyMaxHeartMoreLess = getNumbers("max heart rate", maxheart, 0)

            # Get number of cardio patients more than patient's value.
            cardioMaxHeartMoreLess = getNumbers("max heart rate", maxheart, 1)

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

            # Count fbs 0 and 1 in healthy and cardio patients.
            countHealFBS_0 = countVar("fasting blood sugar",0,0)
            countHealFBS_1 = countVar("fasting blood sugar",0,1)

            countCardioFBS_0 = countVar("fasting blood sugar",1,0)
            countCardioFBS_1 = countVar("fasting blood sugar",1,1)

            healthyFBS = [countHealFBS_0, countHealFBS_1]
            cardioFBS = [countCardioFBS_0, countCardioFBS_1]

            # Count exercise angina 0 and 1 in healthy and cardio patients.
            healthyExang = [countVar("exercise angina",0,0), countVar("exercise angina",0,1)]
            cardioExang = [countVar("exercise angina",1,0), countVar("exercise angina",1,1)]

            return render_template('report_no_login.html', pred = pred, neg = neg, exp = exp, pos = pos, data = data, graphOne = graphOne, healthyChol = healthyChol, healthyAge = healthyAge, cardioChol = cardioChol, cardioAge = cardioAge, rbp = bps, sex = gender, age = age, chol = chol, maxHeart = maxheart, chest = chest, fbs = fbs, oldpeak = oldpeak, exang = exang, stslope = stslope, ecg = ecg, healthyAvg = healthyAvg, cardioAvg = cardioAvg, healthySecAvg = healthySecAvg, cardioSecAvg = cardioSecAvg, graphTwo = graphTwo, healthyRBP = healthyRBP, cardioRBP = cardioRBP, healthyHeart = healthyHeart, cardioHeart = cardioHeart, healthyChest = healthyChest, cardioChest = cardioChest, countHealFBS_0 = countHealFBS_0, countHealFBS_1 = countHealFBS_1, countCardioFBS_0 = countCardioFBS_0, countCardioFBS_1 = countCardioFBS_1, healthyFBS = healthyFBS, cardioFBS = cardioFBS, healthyOldpeak = healthyOldpeak, cardioOldpeak = cardioOldpeak, healthyExang = healthyExang, cardioExang = cardioExang, healthyStSlope = healthyStSlope, cardioStSlope = cardioStSlope, healthyECG = healthyECG, cardioECG = cardioECG, healthyGender = healthyGender, cardioGender = cardioGender, healthyCholMoreLess = healthyCholMoreLess, cardioCholMoreLess = cardioCholMoreLess, healthyRBPMoreLess = healthyRBPMoreLess, cardioRBPMoreLess = cardioRBPMoreLess, healthyMaxHeartMoreLess = healthyMaxHeartMoreLess, cardioMaxHeartMoreLess = cardioMaxHeartMoreLess)

    else:
        # Return no_login form.
        return render_template('no_login.html') 


# Diagnose patient.
@app.route('/diagnose', methods=['GET','POST'])
def diagnose():
    if request.method == 'POST':
        try:
            userID = session['usr']
            # Get patient id.
            pid = request.args.get('pid')
            
            age = db.child(userID).child("Patients").child(pid).child("age").get().val()

            gender = db.child(userID).child("Patients").child(pid).child("gender").get().val()
        
            chest = request.form['chest']
            bps = request.form['bps']
            chol = request.form['chol'] 
            fbs = request.form['fbs']
            ecg = request.form['ecg']
            maxheart = request.form['maxheart']
            exang = request.form['exang']
            oldpeak = request.form['oldpeak']
            stslope = request.form['stslope']


            if((age is not None) and (gender is not None)):
                
                # Get all the values from the form.
                ints = [age, gender, chest, bps, chol, fbs, ecg, maxheart, exang, oldpeak, stslope]
                
                # Check if the list does not contain any empty values and evaluate that all the values are between the limits.
                if all(ints) and check_number(bps, 0, 300) and check_number(chol, 0, 700) and check_number(maxheart, 0, 300) and (0 <= float(oldpeak) <= 7) and check_number(chest, 1, 4) and check_number(fbs, 0, 1) and check_number(ecg, 0, 2) and check_number(exang, 0, 1) and check_number(stslope, 0, 3):
                    # Get current timestamp.
                    ct = int(datetime.datetime.now().timestamp())

                    # Use model to make prediction.
                    final = [np.array(ints)]
                    prediction = model.predict(final)

                    prob_neg = str(model.predict_proba(final)[:,0])[1:-1]
                    prob_pos = str(model.predict_proba(final)[:,1])[1:-1]

                    # Write to the database.
                    if prediction==1:
                        # Save to database.
                        save_to_db(ct, userID, pid, chest, bps, chol, fbs, ecg, maxheart, exang, oldpeak, stslope, 1)
                        # Redirect to the report page.
                        return redirect(url_for('report', pred = "Suffers from a CVD", neg = prob_neg, pos = prob_pos, pid = pid, ct = ct ))
                    else:
                        # Save to database.
                        save_to_db(ct, userID, pid, chest, bps, chol, fbs, ecg, maxheart, exang, oldpeak, stslope, 0)
                        # Redirect to the report page.
                        return redirect(url_for('report', pred= "Most Likely Healthy", neg = prob_neg, pos = prob_pos, pid = pid, ct = ct ))
                else:
                    flash("Please fill all the boxes according to the instructions.", "danger")
                    return redirect(request.url)
            # If age or gender are None, send a message to user.
            else:
                flash("There was a problem fetching some vital patient information.", "danger")
                return redirect(request.url)
        except:
            abort(500)
    else:
        pid = request.args.get('pid')
        if pid is not None:
            return render_template('diagnose.html', pid = pid)
        else:
            flash("Either doctor's or patient's ID were not found.", "danger")
            return redirect(url_for('patients'))

# Patients page.
@app.route('/patients/', methods=['GET','POST'])
def patients():
        if request.method == 'POST':
            # Add a patient.
            try:
                userID = session['usr']
                age = request.form['age']
                gender = request.form['gender']
                
                # Validate input passed in.
                if userID is not None and (0 <= int(gender) <= 1) and (0 <= int(age) <= 120):
                    patient_data = {"age": age, "gender": gender}
                    db.child(userID).child("Patients").push(patient_data)
                    flash("Patient was added.", "success")
                    return redirect(request.url)
                else:
                    # Show error message to user.
                    flash("PATIENT WAS NOT ADDED: Please follow the form's instructions when filling out the form.", "danger")
                    return redirect(request.url)
            except:
                # Show error message to user.
                flash("There was a problem adding the patient", "danger")
                return redirect(request.url)
        else:
            # GET Request.
            return render_template('patients.html')

# Generate visual report.
@app.route('/report')
def report():
    try:
        userID = session['usr']
        pred = request.args.get('pred')
        neg = request.args.get('neg')
        pos = request.args.get('pos')
        pid = request.args.get('pid')
        ct = request.args.get('ct')

        # Get patient.
        patient = db.child(userID).child("Patients").child(pid).get()
        # Get current diagnosis data.
        diagnosisData = db.child(userID).child("Patients").child(pid).child("current").get()

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
        healthyCholMoreLess = getNumbers("cholesterol", diagnosisData.val()['chol'], 0)

        # Get number of cardio patients more than patient's value.
        cardioCholMoreLess = getNumbers("cholesterol", diagnosisData.val()['chol'], 1)

        # Get number of healthy patients more than patient's value.
        healthyRBPMoreLess = getNumbers("resting bp s", diagnosisData.val()['bps'], 0)

        # Get number of cardio patients more than patient's value.
        cardioRBPMoreLess = getNumbers("resting bp s", diagnosisData.val()['bps'], 1)

        # Get number of healthy patients more than patient's value.
        healthyMaxHeartMoreLess = getNumbers("max heart rate", diagnosisData.val()['maxheart'], 0)

        # Get number of cardio patients more than patient's value.
        cardioMaxHeartMoreLess = getNumbers("max heart rate", diagnosisData.val()['maxheart'], 1)

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

        # Count fbs 0 and 1 in healthy and cardio patients.
        countHealFBS_0 = countVar("fasting blood sugar",0,0)
        countHealFBS_1 = countVar("fasting blood sugar",0,1)

        countCardioFBS_0 = countVar("fasting blood sugar",1,0)
        countCardioFBS_1 = countVar("fasting blood sugar",1,1)

        healthyFBS = [countHealFBS_0, countHealFBS_1]
        cardioFBS = [countCardioFBS_0, countCardioFBS_1]

        # Count exercise angina 0 and 1 in healthy and cardio patients.
        healthyExang = [countVar("exercise angina",0,0), countVar("exercise angina",0,1)]
        cardioExang = [countVar("exercise angina",1,0), countVar("exercise angina",1,1)]

        return render_template('report.html', uid = userID, ct = ct, pred = pred, neg = neg, exp = exp, pos = pos, pid = pid, data = data, graphOne = graphOne, healthyChol = healthyChol, healthyAge = healthyAge, cardioChol = cardioChol, cardioAge = cardioAge, rbp = diagnosisData.val()['bps'], sex = patient.val()['gender'], age = patient.val()['age'], chol = diagnosisData.val()['chol'], maxHeart = diagnosisData.val()['maxheart'], chest = diagnosisData.val()['chest'], fbs = diagnosisData.val()['fbs'], oldpeak = diagnosisData.val()['oldpeak'], exang = diagnosisData.val()['exang'], stslope = diagnosisData.val()['stslope'], ecg = diagnosisData.val()['ecg'], healthyAvg = healthyAvg, cardioAvg = cardioAvg, healthySecAvg = healthySecAvg, cardioSecAvg = cardioSecAvg, graphTwo = graphTwo, healthyRBP = healthyRBP, cardioRBP = cardioRBP, healthyHeart = healthyHeart, cardioHeart = cardioHeart, healthyChest = healthyChest, cardioChest = cardioChest, countHealFBS_0 = countHealFBS_0, countHealFBS_1 = countHealFBS_1, countCardioFBS_0 = countCardioFBS_0, countCardioFBS_1 = countCardioFBS_1, healthyFBS = healthyFBS, cardioFBS = cardioFBS, healthyOldpeak = healthyOldpeak, cardioOldpeak = cardioOldpeak, healthyExang = healthyExang, cardioExang = cardioExang, healthyStSlope = healthyStSlope, cardioStSlope = cardioStSlope, healthyECG = healthyECG, cardioECG = cardioECG, healthyGender = healthyGender, cardioGender = cardioGender, healthyCholMoreLess = healthyCholMoreLess, cardioCholMoreLess = cardioCholMoreLess, healthyRBPMoreLess = healthyRBPMoreLess, cardioRBPMoreLess = cardioRBPMoreLess, healthyMaxHeartMoreLess = healthyMaxHeartMoreLess, cardioMaxHeartMoreLess = cardioMaxHeartMoreLess)
    except:
        # Server error.
        abort(500)


# Get patients of user.
@app.route('/getPatients', methods=['GET'])
def getPatients():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    userID = session['usr']
    patients = db.child(userID).child("Patients").get().val()

    return jsonify(patients)


# Add a comment.
@app.route('/report/comments', methods=['POST'])
def report_comments():
    userID = session['usr']
    pid = request.args.get('pid')

    comments = request.form['comments']

    listHistory = []
    snapshot = db.child(userID).child("Patients").child(pid).child("history").get().val()
    for key in snapshot:
        listHistory.append(key)
    
    smallest = getLastId(listHistory)
    db.child(userID).child("Patients").child(pid).child("current").update({"comments":comments})
    db.child(userID).child("Patients").child(pid).child("history").child(smallest).update({"comments":comments})
    
    return ('', 204)

# Save PDF's url to the database.
@app.route('/save_pdf', methods=['POST'])
def save_pdf():
    userID = session['usr']
    pid = request.args.get('pid')
    ct = request.args.get('ct')

    url = request.get_json()
    
    db.child(userID).child("Patients").child(pid).child("current").update({"pdf":url})
    db.child(userID).child("Patients").child(pid).child("history").child(ct).update({"pdf":url})
    
    return ('', 204)

# Get history of patient.
@app.route('/history', methods=['GET'])
def history():
        userID = session['usr']
        pid = request.args.get('pid')
        if userID is not None and pid is not None:
            history = db.child(userID).child("Patients").child(pid).child("history").get().val()
            patient = db.child(userID).child("Patients").child(pid).get().val()
            return render_template('history.html', history = history, pid = pid, patient = patient)
        else:
            flash("Either doctor's or patient's ID were not found.", "danger")
            return redirect(url_for('patients'))
        

# Get specific history.
@app.route('/patients/history/specific')
def history_specific():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    userID = session['usr']
    pid = request.args.get('pid')
    key = request.args.get('key')

    specific = db.child(userID).child("Patients").child(pid).child("history").child(key).get().val()
    return jsonify(specific)


# Get a patient's history.
@app.route('/patients/history', methods=['GET'])
def patients_history():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    userID = session['usr']
    pid = request.args.get('pid')

    history = db.child(userID).child("Patients").child(pid).child("history").get().val()

    return jsonify(history)

# Edit patient.
@app.route('/edit', methods=['GET','POST'])
def edit():
    # Edit patient's data on firebase.
    if request.method == 'POST':
        try:
            userID = session['usr']
            pid = request.args.get('pid')
            age = request.form['age']
            gender = request.form['gender']
                    
            # Validate that data is of the appropriate type.
            if userID is not None and pid is not None and (0 <= int(gender) <= 1) and (0 <= int(age) <= 120):
                patient_data = {"age": age, "gender": gender}
                db.child(userID).child("Patients").child(pid).update(patient_data)

                flash("Patient data was successfully updated!", "success")
                return redirect(request.url)
            else:
                # Show error message to user.
                flash("There was an error with the form, please follow the form's instructions.", "danger")
                return redirect(url_for('patients'))
        except:
            # Server error.
            abort(500)    
    # GET patient's basic information.
    else:
        try:
            userID = session['usr']
            pid = request.args.get('pid')

            # if userID and pid are not None, then return edit form for patient.
            if userID is not None and pid is not None:
                patient = db.child(userID).child("Patients").child(pid).get()

                gender = patient.val()['gender']
                age =  patient.val()['age']

                return render_template('edit.html', pid = pid, gender = gender, age = age)
            else:
                # Show error message to user.
                flash("Either doctor's or patient's ID were not found.", "danger")
                return redirect(url_for('patients'))
        except:
            # Show error message to user.
            abort(500)
            
# Delete a patient.
@app.route('/delete/')
def delete():
    try:
        userID = session['usr']
        pid = request.args.get('pid')

        # if userID and pid are not None, then proceed to delete selected patient.
        if userID is not None and pid is not None:
            db.child(userID).child("Patients").child(pid).remove()
            flash("Patient was deleted successfully.", "success")
            return redirect(url_for('patients'))
        else:
            # Show error message to user.
            flash("There was a problem deleting the patient.", "danger")
            return redirect(url_for('patients'))
    except:
        # Show error message that there was an error deleting the patient.
        flash("There was an error deleting the patient.", "danger")
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)

