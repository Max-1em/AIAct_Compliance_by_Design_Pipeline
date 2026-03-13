from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

data = load_iris()

X = data.data
y = data.target

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "model/model.pkl")

print("Model training completed")
