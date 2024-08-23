import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

import joblib

df = pd.read_csv('dataset.csv')

stats_data = df

X = np.hstack([stats_data.values])
print(X.shape)
y = df['result']

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# save model
joblib.dump(model, 'model.pkl')

# eval model
accuracy = accuracy_score(y_test, model.predict(X_test))
print("Accuracy:", accuracy)
