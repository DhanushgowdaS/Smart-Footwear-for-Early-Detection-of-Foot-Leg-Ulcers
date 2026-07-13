import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load your training data
# Ensure your CSV has columns: 'pressure', 'temp', 'ulcer_risk'
data = pd.read_csv('dataset.csv')

# 2. Define features (X) and target (y)
X = data[['pressure', 'temp']]
y = data['ulcer_risk']  # 0 for safe, 1 for high risk

# 3. Train the model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# 4. Save the model to a file
joblib.dump(model, 'model.pkl')

print("Model trained and saved as model.pkl!")
