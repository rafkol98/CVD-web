import pandas as pd
import numpy as np

df = pd.read_csv("heart_dataset.csv", sep=",")

def getHealthyChol():
    healthy = df[df["target"] == 0]
    chol = list(np.array(healthy["cholesterol"]))
    rbp = list(np.array(healthy["resting bp s"]))
    return np.column_stack((chol, rbp))

# def getCardio():
