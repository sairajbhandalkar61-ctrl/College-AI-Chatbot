# CORTEX 2.0 • Dataset Documentation & Provenance Registry
## Multi-Source Data Architecture for Institutional Analytics

---

## 1. Dataset Provenance & Registry

| Dataset Identifier | Domain | Source / Attribution | Files / Tables | Records / Size | Purpose in CORTEX 2.0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Attendance_Prediction.csv`** | Attendance ML | Institutional Benchmark | `dataset/existing/Attendance_Prediction.csv` | 20,000 rows | Habit-based attendance probability & absence risk factor prediction |
| **`intents1.json`** | NLP Dialogue | Campus Domain Corpus | `dataset/existing/intents1.json` | 78 intent classes, 450+ patterns | Fast on-premise intent classification for campus FAQs & biometric commands |
| **`UCI Student Performance`** | Academic Analytics | P. Cortez & A. Silva (2008), UCI ML Repository | `student-mat.csv`, `student-por.csv` | 1,044 students, 33 features | Final examination grade prediction ($G_3$) and pass/fail risk estimation |
| **`OULAD`** | Learning Analytics | Kuzilek, Hlosta & Zdrahal (2017), Open University | 7 relational tables (`studentVle`, `studentAssessment`, etc.) | 32,593 students, 10.6M LMS interactions | Early course withdrawal & completion likelihood prediction |
| **`CLINC150`** | NLU & Scope Guard | Larson et al. (EMNLP 2019) | `data_full.json`, `data_small.json` | 22,500 utterances, 150 intents + 1,200 OOS | Out-of-scope boundary filter guarding against hallucinations |
| **`O*NET Database`** | Career Intelligence | U.S. Department of Labor / Employment & Training Admin | 6 CSVs (`software_skills`, `knowledge`, etc.) | 10,000+ technology skills | Resume skill extraction, competency scoring, and career pathway matching |
| **`Job Postings`** | Labor Market | Kaggle Online Job Postings Dataset | `data job posts.csv` | 19,000 job postings | Real-world industry skill demand validation |
| **`School Daily Attendance`** | Time-Series Attendance | NYC Open Data / DOE | `2018-2019_Daily_Attendance_20240429.csv` | 1,500+ school days | Macro-level attendance trend benchmarking |
| **`Academic Research PDFs`** | Educational Science | ScienceDirect & arXiv | `102277VOR.pdf`, `Massive.pdf` | Academic Research | Theoretical foundation for Prescriptive Analytics & Multilingual RAG |

---

## 2. Ethical Handling & Synthetic Data Integrity

1. **No Data Fabrication**: Public research datasets (e.g. OULAD, UCI) are strictly used for statistical modeling, pattern discovery, and benchmark inference. They are never represented as actual student records of the institution.
2. **Honest Biometric Disclosure**: Camera feeds and WebAuthn credentials run entirely client-side without storing raw biometric images or templates on the server.
3. **Data Protection**: Personal records are stored locally in relational tables with password hashing and session tokens.
