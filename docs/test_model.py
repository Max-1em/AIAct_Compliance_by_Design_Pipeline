import joblib
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

model = joblib.load("model/model.pkl")

data = load_iris()

pred = model.predict(data.data)

acc = accuracy_score(data.target, pred)

print("Accuracy:", acc)
