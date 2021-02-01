from flask import Flask, render_template
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


@app.route('/predict', methods=['POST','GET'])
def predict():
# Bug with request.
    ints = [int(x) for x in request.form.values()]
    final = [np.array(ints)]
    prediction = model.predict(final)

    if prediction==1:
        return render_template('diagnose.html', pred='Cancer')
    else:
        return render_template('diagnose.html', pred='Healthy')

    

if __name__ == '__main__':
    app.run(debug=True)