import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Create fake patient data

np.random.seed(42)

n = 1000

age = np.random.randint(20, 80, n)
smoking = np.random.randint(0, 2, n)
alcohol = np.random.randint(0, 2, n)
family_history = np.random.randint(0, 2, n)
bmi = np.random.uniform(18, 40, n)
activity = np.random.randint(0, 3, n)

risk = []

for i in range(n):

    score = (
        age[i]*0.03
        + smoking[i]*3
        + alcohol[i]*1.5
        + family_history[i]*3
        + bmi[i]*0.1
        - activity[i]
    )

    if score < 5:
        risk.append(0)

    elif score < 8:
        risk.append(1)

    else:
        risk.append(2)

df = pd.DataFrame({
    "age": age,
    "smoking": smoking,
    "alcohol": alcohol,
    "family_history": family_history,
    "bmi": bmi,
    "activity": activity,
    "risk": risk
})

X = df.drop("risk", axis=1)
y = df["risk"]

model = RandomForestClassifier()

model.fit(X, y)

joblib.dump(model, "cancer_model.pkl")

print("Model created successfully!")