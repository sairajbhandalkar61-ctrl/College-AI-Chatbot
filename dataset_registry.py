"""
dataset_registry.py • Central Dataset Provenance & Path Registry for CORTEX 2.0
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

REGISTRY = {
    'existing': {
        'attendance_prediction': os.path.join(DATASET_DIR, 'existing', 'Attendance_Prediction.csv'),
        'attendance_logs': os.path.join(DATASET_DIR, 'existing', 'attendance_logs.json'),
        'intents': os.path.join(DATASET_DIR, 'existing', 'intents1.json')
    },
    'academic': {
        'oulad': {
            'assessments': os.path.join(DATASET_DIR, 'academic', 'oulad', 'assessments.csv'),
            'courses': os.path.join(DATASET_DIR, 'academic', 'oulad', 'courses.csv'),
            'student_assessment': os.path.join(DATASET_DIR, 'academic', 'oulad', 'studentAssessment.csv'),
            'student_info': os.path.join(DATASET_DIR, 'academic', 'oulad', 'studentInfo.csv'),
            'student_registration': os.path.join(DATASET_DIR, 'academic', 'oulad', 'studentRegistration.csv'),
            'vle': os.path.join(DATASET_DIR, 'academic', 'oulad', 'vle.csv'),
            'student_vle': os.path.join(DATASET_DIR, 'academic', 'oulad', 'studentVle.csv'),
        },
        'student_performance': {
            'math': os.path.join(DATASET_DIR, 'academic', 'student_performance', 'student-mat.csv'),
            'portuguese': os.path.join(DATASET_DIR, 'academic', 'student_performance', 'student-por.csv')
        }
    },
    'attendance': {
        'school_daily': os.path.join(DATASET_DIR, 'attendance', '2018-2019_Daily_Attendance_20240429.csv')
    },
    'chatbot': {
        'clinc150_full': os.path.join(DATASET_DIR, 'chatbot', 'clinc150', 'data', 'data_full.json'),
        'clinc150_small': os.path.join(DATASET_DIR, 'chatbot', 'clinc150', 'data', 'data_small.json')
    },
    'career': {
        'onet': {
            'knowledge': os.path.join(DATASET_DIR, 'career', 'onet', 'knowledge.csv'),
            'essential_skills': os.path.join(DATASET_DIR, 'career', 'onet', 'essential_skills.csv'),
            'transferable_skills': os.path.join(DATASET_DIR, 'career', 'onet', 'transferable_skills.csv'),
            'software_skills': os.path.join(DATASET_DIR, 'career', 'onet', 'software_skills.csv'),
            'specific_interest_areas': os.path.join(DATASET_DIR, 'career', 'onet', 'specific_interest_areas.csv'),
            'career_interest_types': os.path.join(DATASET_DIR, 'career', 'onet', 'career_interest_types.csv')
        },
        'job_postings': os.path.join(DATASET_DIR, 'career', 'job_postings', 'data job posts.csv')
    },
    'research': {
        'prescriptive_analytics_paper': os.path.join(DATASET_DIR, 'research', '102277VOR.pdf'),
        'massive_multilingual_paper': os.path.join(DATASET_DIR, 'research', 'Massive.pdf')
    }
}

def get_dataset_path(*keys):
    """Retrieve absolute path for a registered dataset."""
    curr = REGISTRY
    for k in keys:
        if isinstance(curr, dict) and k in curr:
            curr = curr[k]
        else:
            return None
    return curr if isinstance(curr, str) and os.path.exists(curr) else None

DATASETS = REGISTRY
