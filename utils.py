import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import xgboost as xgb
from imblearn.over_sampling import SMOTE
import os
data = pd.DataFrame({
    'Sleep_Duration': [7, 5, 6, 8, 4, 9, 6, 7],
    'Exercise_Duration': [30, 0, 20, 40, 10, 50, 25, 35],
    'Caffeine_Intake': ['Low', 'High', 'Moderate', 'None', 'High', 'Low', 'Moderate', 'Low'],
    'Screen_Time': [60, 180, 90, 30, 240, 20, 120, 50],
    'Stress_Level': [3, 8, 5, 2, 9, 1, 4, 3],
    'Sleep_Quality': ['Good', 'Poor', 'Average', 'Good', 'Poor', 'Good', 'Average', 'Good']
})

le_caffeine = LabelEncoder()
data['Caffeine_Intake'] = le_caffeine.fit_transform(data['Caffeine_Intake'])

le_quality = LabelEncoder()
data['Sleep_Quality'] = le_quality.fit_transform(data['Sleep_Quality'])

X = data.drop('Sleep_Quality', axis=1)
y = data['Sleep_Quality']

smote = SMOTE(random_state=42, k_neighbors=1)
X_res, y_res = smote.fit_resample(X, y)


X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)


model = xgb.XGBClassifier(
    use_label_encoder=False, 
    eval_metric='mlogloss', 
    random_state=42
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/sleep_model.pkl')
print("Model saved at models/sleep_model.pkl")
