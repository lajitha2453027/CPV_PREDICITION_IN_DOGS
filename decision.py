import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Load dataset
data = pd.read_csv("dataset.csv")

# Features and target
X = data[['vomiting','diarrhea','fever',
          'loss_appetite','lethargy','dehydration']]
y = data['cpv']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Metrics
print("Model: Decision Tree")
print("Accuracy: {:.2f}".format(accuracy_score(y_test, y_pred)*100))
print("Recall: {:.2f}".format(recall_score(y_test, y_pred)*100))
print("Precision: {:.2f}".format(precision_score(y_test, y_pred)*100))

# =========================
# 🔷 CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# Plot Confusion Matrix (MATLAB-style grid)
plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# Show values inside boxes
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i, j], ha='center', va='center')

plt.xticks([0,1])
plt.yticks([0,1])
plt.show()

# =========================
# 🔷 HISTOGRAM (Predictions)
# =========================
plt.figure()
plt.hist(y_pred, bins=2)
plt.title("Prediction Distribution")
plt.xlabel("Class (0 = No CPV, 1 = CPV)")
plt.ylabel("Frequency")
plt.show()