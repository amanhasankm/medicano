# train_diabetes.py (debug version)
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

try:
    from xgboost import XGBClassifier
    has_xgb = True
except Exception:
    has_xgb = False
    XGBClassifier = None

print("📂 Loading dataset...")
DATA_PATH = "diabetes.csv"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print(f"✅ Dataset loaded with shape: {df.shape}")

if 'Outcome' not in df.columns:
    raise ValueError("Expected column 'Outcome' in CSV")

print("🧹 Cleaning data...")
cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for c in cols_with_zero:
    if c in df.columns:
        df[c] = df[c].replace(0, np.nan)
        df[c].fillna(df[c].median(), inplace=True)

X = df.drop('Outcome', axis=1)
y = df['Outcome']

print("📊 Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

print("🤖 Training models...")
models = {}
param_grids = {}

models['logreg'] = LogisticRegression(max_iter=2000, solver='liblinear')
param_grids['logreg'] = {
    'clf__C': [0.01, 0.1, 1.0, 10],
    'clf__penalty': ['l2']
}

models['rf'] = RandomForestClassifier(random_state=42)
param_grids['rf'] = {
    'clf__n_estimators': [100, 200],
    'clf__max_depth': [None, 5, 10]
}

if has_xgb:
    models['xgb'] = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    param_grids['xgb'] = {
        'clf__n_estimators': [100, 200],
        'clf__max_depth': [3, 6],
        'clf__learning_rate': [0.01, 0.1]
    }

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
best_overall = None
best_score = -1

for name, model in models.items():
    print(f"\n🚀 Training {name} ...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', model)
    ])
    try:
        grid = GridSearchCV(pipeline, param_grids[name], cv=cv, scoring='roc_auc', n_jobs=-1, verbose=1)
        grid.fit(X_train, y_train)
    except Exception as e:
        print(f"❌ Error training {name}: {e}")
        continue

    best = grid.best_estimator_
    y_pred = best.predict(X_test)
    y_proba = best.predict_proba(X_test)[:, 1]
    roc = roc_auc_score(y_test, y_proba)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ {name} - Best Params: {grid.best_params_}")
    print(f"📈 ROC-AUC: {roc:.4f} | Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    if roc > best_score:
        best_score = roc
        best_overall = (name, best)

if best_overall is None:
    raise RuntimeError("No model was successfully trained.")

best_name, best_pipeline = best_overall
out_path = "DiabetesChecker/diabetes_pipeline.joblib"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
joblib.dump(best_pipeline, out_path)

print(f"\n💾 Saved best model ({best_name}) to {out_path} with ROC-AUC={best_score:.4f}")
