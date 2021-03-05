import pandas as pd
import numpy as np

df = pd.read_csv("heart_dataset.csv", sep=",")

def getChol(pred):
    data = df[df["target"] == pred]
    chol = list(np.array(data["cholesterol"]))
    # rbp = list(np.array(healthy["resting bp s"]))
    return chol

def getRBP(pred):
    data = df[df["target"] == pred]
    # chol = list(np.array(healthy["cholesterol"]))
    rbp = list(np.array(data["age"]))
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

# Get average for all values in the dataset.
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
