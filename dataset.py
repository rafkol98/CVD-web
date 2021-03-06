import pandas as pd
import numpy as np

df = pd.read_csv("heart_dataset.csv", sep=",")

def getChol(pred):
    data = df[df["target"] == pred]
    chol = list(np.array(data["cholesterol"]))
    return chol

def getAge(pred):
    data = df[df["target"] == pred]
    age = list(np.array(data["age"]))
    return age

def getRBP(pred):
    data = df[df["target"] == pred]
    rbp = list(np.array(data["resting bp s"]))
    return rbp

# Get average for all values in the dataset.
def getAvg(pred):
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


