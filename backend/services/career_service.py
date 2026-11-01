"""
backend/services/career_service.py • O*NET Career Guidance & Resume Gap Engine for CORTEX 2.0
Analyzes student skill profiles against O*NET occupational benchmarks and job postings.
"""
import os
import re
import pandas as pd
from collections import Counter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ONET_DIR = os.path.join(BASE_DIR, 'dataset', 'career', 'onet')

class CareerService:
    def __init__(self):
        self.occupation_skills = {}
        self.popular_skills = []
        self.load_onet_taxonomy()

    def load_onet_taxonomy(self):
        sk_path = os.path.join(ONET_DIR, 'software_skills.csv')
        if not os.path.exists(sk_path):
            return

        try:
            df = pd.read_csv(sk_path)
            # Filter for computer/tech occupations
            tech_df = df[df['Title'].str.contains('Software|Data|Computer|Developer|Information|Network|Web', case=False, na=False)]
            
            for title, group in tech_df.groupby('Title'):
                skills = group['Workplace Example'].dropna().unique().tolist()
                self.occupation_skills[title] = skills
                
            self.popular_skills = [
                'Python', 'Java', 'C++', 'SQL', 'JavaScript', 'React', 'Node.js',
                'Machine Learning', 'TensorFlow', 'PyTorch', 'Docker', 'Kubernetes',
                'AWS', 'Git', 'Linux', 'Data Structures', 'Algorithms', 'Flask'
            ]
        except Exception as e:
            print("Warning loading O*NET taxonomy:", e)

    def extract_skills_from_text(self, text):
        """Extracts technical skills by matching against the standardized taxonomy."""
        if not text:
            return []
        found = set()
        clean_text = text.lower()
        
        # Check standard dictionary
        for skill in self.popular_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, clean_text):
                found.add(skill)
                
        # Also check extracted O*NET skills
        for occ, skills in list(self.occupation_skills.items())[:15]:
            for s in skills[:30]:
                if len(s) > 2 and re.search(r'\b' + re.escape(s.lower()) + r'\b', clean_text):
                    found.add(s)
                    
        return sorted(list(found))

    def match_career_roles(self, user_skills):
        """Matches user skills against O*NET occupations and calculates gap analysis."""
        user_set = set(s.lower() for s in user_skills)
        if not user_set:
            user_set = {'python', 'sql', 'machine learning', 'data structures', 'flask'}

        # Target benchmarks
        target_roles = {
            'Machine Learning Engineer': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'SQL', 'Docker', 'Git', 'Data Structures'],
            'Full-Stack Software Developer': ['JavaScript', 'React', 'Node.js', 'Python', 'SQL', 'Git', 'Docker', 'Linux'],
            'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Data Structures', 'Statistics', 'Pandas', 'Tableau'],
            'Cloud & DevOps Engineer': ['Linux', 'Docker', 'Kubernetes', 'AWS', 'Python', 'Git', 'CI/CD'],
            'Database Administrator': ['SQL', 'Database Management', 'Linux', 'Python', 'Performance Tuning', 'Backup & Recovery']
        }

        matches = []
        for role, required in target_roles.items():
            req_set = set(r.lower() for r in required)
            matched = [r for r in required if r.lower() in user_set]
            missing = [r for r in required if r.lower() not in user_set]
            match_score = round((len(matched) / max(1, len(required))) * 100, 1)

            matches.append({
                'role': role,
                'match_percentage': match_score,
                'matching_skills': matched,
                'missing_skills': missing,
                'readiness_level': 'High Match' if match_score >= 70 else ('Moderate Match' if match_score >= 50 else 'Developing'),
                'recommended_next_step': f"Learn {missing[0]} and build a showcase project" if missing else "Ready for campus interview applications"
            })

        matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        return matches

# Global singleton
career_engine = CareerService()
