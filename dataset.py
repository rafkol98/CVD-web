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
    average =  list(np.array(data.mean()))
    return average
