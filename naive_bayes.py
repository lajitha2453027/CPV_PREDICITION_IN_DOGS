import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv("dataset.csv")

X = data[['vomiting','diarrhea','fever',
          'loss_appetite','lethargy','dehydration']]
y = data['cpv']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = GaussianNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Model: Naive Bayes")
print("Accuracy: {:.2f}".format(accuracy_score(y_test, y_pred)*100))
print("Recall: {:.2f}".format(recall_score(y_test, y_pred, average='binary')*100))
print("Precision: {:.2f}".format(precision_score(y_test, y_pred, average='binary')*100))
