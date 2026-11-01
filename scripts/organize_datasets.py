import os
import zipfile
import shutil
import glob
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

# Define target directories
TARGET_DIRS = {
    'existing': os.path.join(DATASET_DIR, 'existing'),
    'oulad': os.path.join(DATASET_DIR, 'academic', 'oulad'),
    'student_perf': os.path.join(DATASET_DIR, 'academic', 'student_performance'),
    'attendance': os.path.join(DATASET_DIR, 'attendance'),
    'clinc150': os.path.join(DATASET_DIR, 'chatbot', 'clinc150'),
    'job_postings': os.path.join(DATASET_DIR, 'career', 'job_postings'),
    'onet': os.path.join(DATASET_DIR, 'career', 'onet'),
    'research': os.path.join(DATASET_DIR, 'research')
}

for d in TARGET_DIRS.values():
    os.makedirs(d, exist_ok=True)

print("Target directories created.")

# 1. Existing baseline dataset files
for fname in ['Attendance_Prediction.csv', 'attendance_logs.json', 'intents1.json']:
    src = os.path.join(DATASET_DIR, fname)
    if os.path.exists(src):
        dst = os.path.join(TARGET_DIRS['existing'], fname)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Preserved baseline file: {fname} -> dataset/existing/")

# 2. Extract OULAD
oulad_zip = os.path.join(DATASET_DIR, 'open+university+learning+analytics+dataset.zip')
if os.path.exists(oulad_zip):
    print("Extracting OULAD dataset...")
    with zipfile.ZipFile(oulad_zip, 'r') as zf:
        zf.extractall(TARGET_DIRS['oulad'])
    print(f"Extracted OULAD to {TARGET_DIRS['oulad']}")

# 3. Extract Student Performance
perf_zip = os.path.join(DATASET_DIR, 'student_performance.zip')
if os.path.exists(perf_zip):
    print("Extracting student_performance.zip...")
    with zipfile.ZipFile(perf_zip, 'r') as zf:
        zf.extractall(TARGET_DIRS['student_perf'])

perf_zip_uci = os.path.join(DATASET_DIR, 'student+performance.zip')
if os.path.exists(perf_zip_uci):
    print("Extracting student+performance.zip...")
    with zipfile.ZipFile(perf_zip_uci, 'r') as zf:
        zf.extractall(TARGET_DIRS['student_perf'])
    # Check for inner student.zip
    inner_zip = os.path.join(TARGET_DIRS['student_perf'], 'student.zip')
    if os.path.exists(inner_zip):
        with zipfile.ZipFile(inner_zip, 'r') as zf:
            zf.extractall(TARGET_DIRS['student_perf'])
        print("Extracted inner student.zip successfully.")

# 4. Extract School Attendance
att_zip = os.path.join(DATASET_DIR, 'student_attendance.zip')
if os.path.exists(att_zip):
    print("Extracting student_attendance.zip...")
    with zipfile.ZipFile(att_zip, 'r') as zf:
        zf.extractall(TARGET_DIRS['attendance'])

# 5. Extract CLINC150
clinc_zip = os.path.join(DATASET_DIR, 'oos-eval-master.zip')
if os.path.exists(clinc_zip):
    print("Extracting CLINC150 oos-eval-master.zip...")
    with zipfile.ZipFile(clinc_zip, 'r') as zf:
        zf.extractall(TARGET_DIRS['clinc150'])

# 6. Extract Job Postings
job_zip = os.path.join(DATASET_DIR, 'job_posting.zip')
if os.path.exists(job_zip):
    print("Extracting job_posting.zip...")
    with zipfile.ZipFile(job_zip, 'r') as zf:
        zf.extractall(TARGET_DIRS['job_postings'])

# 7. Organize O*NET CSV files
onet_files = [
    'knowledge.csv', 'essential_skills.csv', 'transferable_skills.csv',
    'software_skills.csv', 'specific_interest_areas.csv', 'career_interest_types.csv',
    'career_interest_type_keywords.csv', 'interests_illustrative_activities.csv',
    'interests_illustrative_occupations.csv', 'specific_interest_areas_to_career_interest_types.csv'
]
for ofile in onet_files:
    src = os.path.join(DATASET_DIR, ofile)
    if os.path.exists(src):
        dst = os.path.join(TARGET_DIRS['onet'], ofile)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Organized O*NET file: {ofile} -> dataset/career/onet/")

# 8. Organize Research PDFs
for pdf_file in ['102277VOR.pdf', 'Massive.pdf']:
    src = os.path.join(DATASET_DIR, pdf_file)
    if os.path.exists(src):
        dst = os.path.join(TARGET_DIRS['research'], pdf_file)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Organized research paper: {pdf_file} -> dataset/research/")

print("Dataset organization completed successfully.")
