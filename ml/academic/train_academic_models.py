"""
ml/academic/train_academic_models.py
Trains academic performance models using UCI Student Performance and OULAD datasets.
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, classification_report

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_uci_grade_model():
    print("=" * 60)
    print("1. Training UCI Student Performance Grade Predictor...")
    print("=" * 60)
    
    mat_path = os.path.join(DATASET_DIR, 'academic', 'student_performance', 'student-mat.csv')
    por_path = os.path.join(DATASET_DIR, 'academic', 'student_performance', 'student-por.csv')
    
    df_mat = pd.read_csv(mat_path, sep=';')
    df_mat['subject'] = 'math'
    df_por = pd.read_csv(por_path, sep=';')
    df_por['subject'] = 'portuguese'
    
    df = pd.concat([df_mat, df_por], ignore_index=True)
    print(f"Loaded {len(df)} total student records (Math + Portuguese).")
    
    # Feature Selection (Avoiding target leakage from G3 while utilizing G1, G2 and behavioral factors)
    features = [
        'studytime', 'failures', 'absences', 'traveltime', 'age',
        'Medu', 'Fedu', 'freetime', 'goout', 'health', 'internet', 'higher', 'subject', 'G1', 'G2'
    ]
    
    categorical = ['internet', 'higher', 'subject']
    numerical = [c for c in features if c not in categorical]
    
    X = df[features]
    y = df['G3']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first'), categorical),
            ('num', 'passthrough', numerical)
        ]
    )
    
    reg_pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    reg_pipeline.fit(X_train, y_train)
    
    y_pred = reg_pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Grade Regression Evaluation: MAE = {mae:.2f} points (scale 0-20), R2 = {r2:.3f}")
    
    # Classification pipeline (Pass >= 10, At-Risk < 10)
    clf_pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42))
    ])
    y_class_train = (y_train >= 10).astype(int)
    y_class_test = (y_test >= 10).astype(int)
    clf_pipeline.fit(X_train, y_class_train)
    acc = accuracy_score(y_class_test, clf_pipeline.predict(X_test))
    print(f"Pass/Fail Classification Accuracy: {acc*100:.2f}%")
    
    return reg_pipeline, clf_pipeline, features

def train_oulad_outcome_model():
    print("\n" + "=" * 60)
    print("2. Training OULAD Course Outcome & Completion Predictor...")
    print("=" * 60)
    
    oulad_dir = os.path.join(DATASET_DIR, 'academic', 'oulad')
    df_info = pd.read_csv(os.path.join(oulad_dir, 'studentInfo.csv'))
    df_assess = pd.read_csv(os.path.join(oulad_dir, 'studentAssessment.csv'))
    
    # Ensure score is numeric
    df_assess['score'] = pd.to_numeric(df_assess['score'], errors='coerce')

    # Aggregate assessment scores per student
    avg_scores = df_assess.groupby('id_student')['score'].mean().reset_index()
    avg_scores.columns = ['id_student', 'avg_assessment_score']
    
    # Merge student info with average assessment score
    df = pd.merge(df_info, avg_scores, on='id_student', how='left')
    df['avg_assessment_score'] = df['avg_assessment_score'].fillna(df['avg_assessment_score'].median())
    
    # Binary Target: 1 = Success (Pass/Distinction), 0 = At-Risk (Fail/Withdrawn)
    df['is_success'] = df['final_result'].isin(['Pass', 'Distinction']).astype(int)
    
    features = ['highest_education', 'age_band', 'num_of_prev_attempts', 'studied_credits', 'avg_assessment_score']
    X = df[features]
    y = df['is_success']
    
    categorical = ['highest_education', 'age_band']
    numerical = ['num_of_prev_attempts', 'studied_credits', 'avg_assessment_score']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
            ('num', 'passthrough', numerical)
        ]
    )
    
    oulad_pipeline = Pipeline([
        ('prep', preprocessor),
        ('model', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    oulad_pipeline.fit(X_train, y_train)
    
    y_pred = oulad_pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"OULAD Success Prediction Accuracy: {acc*100:.2f}%")
    print(classification_report(y_test, y_pred, target_names=['At-Risk', 'Success']))
    
    return oulad_pipeline, features

def main():
    uci_reg, uci_clf, uci_feats = train_uci_grade_model()
    oulad_clf, oulad_feats = train_oulad_outcome_model()
    
    artifacts = {
        'uci_regressor': uci_reg,
        'uci_classifier': uci_clf,
        'uci_features': uci_feats,
        'oulad_classifier': oulad_clf,
        'oulad_features': oulad_feats
    }
    
    out_path = os.path.join(MODEL_DIR, 'academic_models.pkl')
    with open(out_path, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"\n[Saved Model Artifacts] {out_path}")

if __name__ == '__main__':
    main()
