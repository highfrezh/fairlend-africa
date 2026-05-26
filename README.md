# 🌍 FairLend-Africa
**Explainable AI for Alternative Credit Scoring in Financially Excluded Communities**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-EE4C2C)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Overview
Access to formal credit is a fundamental barrier to financial inclusion in Sub-Saharan Africa. **FairLend-Africa** is a research-grade framework that proves how behavioral data—mobile money transactions, savings consistency, and airtime habits—can serve as powerful, fair, and explainable proxies for creditworthiness.

> [!NOTE] 
> This is a **Research Demonstration Project** developed for academic transparency and to showcase high-stakes AI auditing. It is not intended for commercial use.

### 🧪 Research at a Glance
| Metric | Performance |
| :--- | :--- |
| **Model Ranking (ROC-AUC)** | **0.7137** (Peer-benchmarked) |
| **Decision Precision** | **86.0%** |
| **Fairness Compliance** | **100%** (Zero violations of the 80% rule) |
| **Primary Signal** | `wallet_balance_trend` (SHAP: 0.377) |

---

## 🖥️ Dashboard Preview
![Dashboard Mockup](https://raw.githubusercontent.com/highfrezh/fairlend-africa/main/artifacts/evaluation/model_comparison.png)
*The FairLend Dashboard provides loan officers with real-time SHAP-based explanations for every credit decision, bridging the gap between "Black Box" AI and human understanding.*

---

## 🏗️ Project Architecture
```text
fairlend-africa/
├── notebooks/        # End-to-end research pipeline (01-06)
├── api/              # High-performance FastAPI backend
├── frontend/         # Interactive React dashboard
├── src/              # Core logic for data & ML auditing
├── artifacts/        # Generated plots, metrics, and serialized models
└── paper/            # 📄 fairlend_africa.pdf (Manuscript)
```

---

## 🚀 Quick Start (Reproduction Guide)

### 1. Environment Setup
```bash
git clone https://github.com/highfrezh/fairlend-africa.git
cd fairlend-africa
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate Data & Train Model
```bash
# Generate 10,000 synthetic behavioral records
python src/data/generate_dataset.py --n 10000

# Execute the pipeline (or open notebooks/ to view)
# Highly recommended: notebooks/05_shap_analysis.ipynb
```

### 3. Launch the System
```bash
# Start API (Port 8001)
uvicorn api.main:app --reload --port 8001

# Start Dashboard (New Terminal)
cd frontend && npm install && npm run dev
```

---

## ⚖️ Fairness & Ethics
Unlike black-box scoring systems, FairLend-Africa includes a **Systematic Fairness Audit**. We test for demographic parity across gender and regional subgroups (West, East, Central, Southern Africa). 

Our findings demonstrate that by excluding demographic features from model inputs and focusing on behavioral discipline, we can achieve a baseline of **Zero Fairness Violations** based on the 80% rule benchmark.

---

## 📄 Citation
If using this framework for research, please cite the work as follows:

```bibtex
@techreport{olabintan2026fairlend,
  author = {Olabintan, Ibraheem},
  title = {FairLend-Africa: An Explainable Machine Learning Framework for Alternative Credit Scoring},
  institution = {Kebbi State University of Science and Technology Aliero},
  year = {2026},
  type = {Research Portfolio}
}
```

---

## 👤 Author
**Ibraheem Olabintan**  
*Department of Computer Science*  
**Kebbi State University of Science and Technology.**  
Aliero, Kebbi State, Nigeria  

---
*Developed with a focus on Algorithm Transparency, Financial Inclusion, and Scalable Fintech.*
