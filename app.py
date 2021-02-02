from flask import Flask, render_template, request
import pickle
import numpy as np

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
    
    output = model.predict_proba(final)
    if prediction==1:
        return render_template('report.html', pred = "Suffers from a CVD", prob = output )
    else:
        return render_template('report.html', pred= "Most Likely Healthy", prob = output )

    

if __name__ == '__main__':
    app.run(debug=True)