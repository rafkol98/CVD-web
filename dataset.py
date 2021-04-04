import pandas as pd
import numpy as np

df = pd.read_csv("dataset.csv", sep=",")

# Get all the values of patients with the given prediction.
def getVar(variable,pred):
    data = df[df["target"] == pred]
    return list(np.array(data[variable]))

# count how many patients there are in the given variable with the given value.
def countVar(variable, pred, value):
    data = df[df["target"] == pred]
    x = list(np.array(data[variable]))
    return x.count(value)

# Get number of patients that have a value higher than the patient's value for the variable passed in.
def getNumberPatientsMore(variable, patient_value, condition):
    data = df[df["target"] == condition]
    x = list(np.array(data[variable]))
    return sum(i > int(patient_value) for i in x)

def getNumberPatientsLess(variable, patient_value, condition):
    data = df[df["target"] == condition]
    x = list(np.array(data[variable]))
    return sum(i <= int(patient_value) for i in x)

# Get average for all values in the dataset.
def firstGraph(pred):
    data = df[df["target"] == pred]
    data = data.drop('target', 1)
    data = data.drop('max heart rate', 1)
    data = data.drop('resting bp s', 1)
    data = data.drop('cholesterol', 1)

    average =  list(np.array(data.mean()))

    # drop first two elements.
    first_item = average.pop(0)
    second_item = average.pop(0)
    return average

# Get average for all values in the dataset.
# TODO : Clean this!
def secondGraph(pred):
    data = df[df["target"] == pred]
    data = data.drop('target', 1)
    data = data.drop('chest pain type', 1)
    data = data.drop('fasting blood sugar', 1)
    data = data.drop('resting ecg', 1)
    data = data.drop('exercise angina', 1)
    data = data.drop('oldpeak', 1)
    data = data.drop('ST slope', 1)

    average =  list(np.array(data.mean()))

    # drop first two elements.
    first_item = average.pop(0)
    second_item = average.pop(0)

    return average


