import os
import glob
import json
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

def inspect_csv(path, sep=','):
    try:
        df = pd.read_csv(path, sep=sep, nrows=1000)
        total_rows = sum(1 for _ in open(path, 'r', encoding='utf-8', errors='ignore')) - 1
        return {
            'file': os.path.basename(path),
            'path': os.path.relpath(path, BASE_DIR),
            'total_rows': total_rows,
            'sample_cols': list(df.columns),
            'col_count': len(df.columns),
            'missing_cols': df.isnull().sum()[df.isnull().sum() > 0].to_dict()
        }
    except Exception as e:
        return {'file': os.path.basename(path), 'error': str(e)}

def run_validation():
    registry = {}
    print("=" * 70)
    print("CORTEX 2.0 DATASET PROFILING & VALIDATION AUDIT")
    print("=" * 70)

    # 1. Existing Attendance Dataset
    att_csv = os.path.join(DATASET_DIR, 'existing', 'Attendance_Prediction.csv')
    if os.path.exists(att_csv):
        info = inspect_csv(att_csv)
        registry['existing_attendance'] = info
        print(f"[Existing Attendance] {info['file']}: {info['total_rows']} rows, {info['col_count']} cols.")

    # 2. OULAD
    oulad_files = glob.glob(os.path.join(DATASET_DIR, 'academic', 'oulad', '*.csv'))
    registry['oulad'] = []
    print(f"\n[OULAD] Found {len(oulad_files)} tables:")
    for f in oulad_files:
        info = inspect_csv(f)
        registry['oulad'].append(info)
        print(f"  • {info['file']}: {info.get('total_rows', 'N/A')} rows, cols: {info.get('col_count')}")

    # 3. Student Performance (UCI)
    perf_files = glob.glob(os.path.join(DATASET_DIR, 'academic', 'student_performance', '*.csv'))
    registry['student_performance'] = []
    print(f"\n[Student Performance] Found {len(perf_files)} files:")
    for f in perf_files:
        # Check delimiter (; or ,)
        sep = ';' if 'student-' in f else ','
        info = inspect_csv(f, sep=sep)
        registry['student_performance'].append(info)
        print(f"  • {info['file']}: {info.get('total_rows', 'N/A')} rows, cols: {info.get('col_count')}")

    # 4. School Daily Attendance
    sch_att_files = glob.glob(os.path.join(DATASET_DIR, 'attendance', '*.csv'))
    registry['school_attendance'] = []
    print(f"\n[School Daily Attendance] Found {len(sch_att_files)} files:")
    for f in sch_att_files:
        info = inspect_csv(f)
        registry['school_attendance'].append(info)
        print(f"  • {info['file']}: {info.get('total_rows', 'N/A')} rows, cols: {info.get('col_count')}")

    # 5. CLINC150
    clinc_jsons = glob.glob(os.path.join(DATASET_DIR, 'chatbot', 'clinc150', '**', '*.json'), recursive=True)
    registry['clinc150'] = []
    print(f"\n[CLINC150] Found {len(clinc_jsons)} JSON files:")
    for jf in clinc_jsons:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            sample_keys = list(data.keys())
            train_count = len(data.get('train', []))
            val_count = len(data.get('val', []))
            test_count = len(data.get('test', []))
            oos_count = len(data.get('oos_test', []))
            rel = os.path.relpath(jf, BASE_DIR)
            registry['clinc150'].append({
                'file': os.path.basename(jf),
                'path': rel,
                'splits': sample_keys,
                'counts': {'train': train_count, 'val': val_count, 'test': test_count, 'oos_test': oos_count}
            })
            print(f"  • {os.path.basename(jf)}: train={train_count}, val={val_count}, test={test_count}, oos={oos_count}")
        except Exception as e:
            pass

    # 6. O*NET Career Datasets
    onet_files = glob.glob(os.path.join(DATASET_DIR, 'career', 'onet', '*.csv'))
    registry['onet'] = []
    print(f"\n[O*NET Career Intelligence] Found {len(onet_files)} tables:")
    for f in onet_files:
        info = inspect_csv(f)
        registry['onet'].append(info)
        print(f"  • {info['file']}: {info.get('total_rows', 'N/A')} rows, cols: {info.get('col_count')}")

    # 7. Job Postings
    job_files = glob.glob(os.path.join(DATASET_DIR, 'career', 'job_postings', '*.csv'))
    registry['job_postings'] = []
    print(f"\n[Job Postings] Found {len(job_files)} files:")
    for f in job_files:
        info = inspect_csv(f)
        registry['job_postings'].append(info)
        print(f"  • {info['file']}: {info.get('total_rows', 'N/A')} rows, cols: {info.get('col_count')}")

    # Save registry JSON
    reg_out = os.path.join(DATASET_DIR, 'dataset_registry.json')
    with open(reg_out, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    print(f"\n[Saved Registry] dataset/dataset_registry.json")
    print("=" * 70)

if __name__ == '__main__':
    run_validation()
