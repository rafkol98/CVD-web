import pandas as pd
import numpy as np

df = pd.read_csv("heart_dataset.csv", sep=",")

def getChol(pred):
    healthy = df[df["target"] == pred]
    chol = list(np.array(healthy["cholesterol"]))
    # rbp = list(np.array(healthy["resting bp s"]))
    return chol

def getRBP(pred):
    healthy = df[df["target"] == pred]
    # chol = list(np.array(healthy["cholesterol"]))
    rbp = list(np.array(healthy["resting bp s"]))
    return rbp

# def getCardio():
