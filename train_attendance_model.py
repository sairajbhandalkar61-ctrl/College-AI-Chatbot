import csv
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

print("Loading dataset/Attendance_Prediction.csv...")
features = []
y_attendance = []
y_reason = []

with open('dataset/Attendance_Prediction.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        feat = {
            'age': float(row['age']) if row['age'] else 20.0,
            'course': row['course'].strip().lower(),
            'year': row['year'].strip().lower(),
            'parent_education': row['parent_education'].strip().lower(),
            'internet_access': row['internet_access'].strip().lower(),
            'hostel_resident': row['hostel_resident'].strip().lower(),
            'class_type': row['class_type'].strip().lower(),
            'weather': row['weather'].strip().lower(),
            'study_hours': float(row['study_hours']) if row['study_hours'] else 3.0,
            'sleep_hours': float(row['sleep_hours']) if row['sleep_hours'] else 7.0,
            'travel_time_minutes': float(row['travel_time_minutes']) if row['travel_time_minutes'] else 30.0
        }
        features.append(feat)
        y_attendance.append(int(row['attendance']))
        y_reason.append(row['absence_reason'].strip().lower())

print(f"Loaded {len(features)} records.")

vec = DictVectorizer(sparse=False)
X = vec.fit_transform(features)

X_train, X_test, y_train, y_test, r_train, r_test = train_test_split(
    X, y_attendance, y_reason, test_size=0.2, random_state=42
)

print("Training Attendance Prediction Classifier (RandomForest)...")
rf_attendance = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
rf_attendance.fit(X_train, y_train)

y_pred = rf_attendance.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Attendance Model Accuracy: {acc*100:.2f}%")
print(classification_report(y_test, y_pred))

# Train Absence Reason Classifier for students who are absent (attendance == 0)
absent_indices_train = [i for i, att in enumerate(y_train) if att == 0]
X_train_absent = X_train[absent_indices_train]
r_train_absent = [r_train[i] for i in absent_indices_train]

print("Training Absence Reason Predictor...")
rf_reason = RandomForestClassifier(n_estimators=80, max_depth=10, random_state=42, n_jobs=-1)
rf_reason.fit(X_train_absent, r_train_absent)

# Save artifacts
artifacts = {
    'vectorizer': vec,
    'feature_keys': list(features[0].keys()),
    'unique_courses': sorted(list(set(f['course'] for f in features))),
    'unique_years': sorted(list(set(f['year'] for f in features))),
    'unique_class_types': sorted(list(set(f['class_type'] for f in features))),
    'unique_weather': sorted(list(set(f['weather'] for f in features)))
}

with open('model/attendance_encoder.pkl', 'wb') as f:
    pickle.dump(artifacts, f)

model_payload = {
    'attendance_model': rf_attendance,
    'reason_model': rf_reason
}

with open('model/attendance_model.pkl', 'wb') as f:
    pickle.dump(model_payload, f)

print("Artifacts successfully saved to model/attendance_encoder.pkl and model/attendance_model.pkl")
