import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

print("Training Multiple Algorithms...")

data = pd.read_csv("dataset.csv")

X = data[['vomiting','diarrhea','fever',
          'loss_appetite','lethargy','dehydration']]
y = data['cpv']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Models
models = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "Naive Bayes": GaussianNB(),
    "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42)
}

best_model = None
best_accuracy = 0
best_name = ""

print("\nModel\t\tAccuracy\tRecall\tPrecision\tF1 Score")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred) * 100
    rec = recall_score(y_test, y_pred, average='binary') * 100
    pre = precision_score(y_test, y_pred, average='binary') * 100
    f1 = f1_score(y_test, y_pred, average='binary') * 100

    cm = confusion_matrix(y_test, y_pred)

    print(f"{name:15} {acc:.2f}\t\t{rec:.2f}\t{pre:.2f}\t\t{f1:.2f}")
    print("Confusion Matrix:")
    print(cm)
    print("-"*50)

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model
        best_name = name

# Save Best Model
with open("best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("\nBest Algorithm Selected:", best_name)
print("Best Accuracy: {:.2f}%".format(best_accuracy))
print("Best model saved as best_model.pkl")

