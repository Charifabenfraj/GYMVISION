# 🏋️ Gym Membership Analytics – Machine Learning Web Application

A Django-based web application that leverages Machine Learning to analyze gym membership data, predict customer churn, segment members, and estimate customer satisfaction.

## 🚀 Key Features

- **Churn Prediction:** Identify members at risk of leaving the gym using XGBoost.
- **Customer Segmentation:** Group members into 4 clusters using K-Means.
- **Satisfaction Prediction:** Predict customer satisfaction levels (Low, Medium, High).
- **Personalized Recommendations:** Provide retention strategies and marketing suggestions.
- **Interactive Dashboard:** Visualize customer profiles, statistics, and clustering results.
- **Model Persistence:** Save and reuse trained ML models using Pickle (`.pkl`).
- **Automatic Model Training:** Train and save models through custom Django commands.

## 🧠 Machine Learning Models

| Model | Algorithm | Purpose |
|---|---|---|
| Churn Prediction | XGBoost | Predict customer churn |
| Customer Segmentation | K-Means | Identify 4 customer groups |
| Satisfaction Prediction | XGBoost | Estimate satisfaction levels |

## 🛠️ Technologies

- **Backend:** Python, Django
- **Machine Learning:** XGBoost, Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Model Persistence:** Pickle

## 📊 Application Modules

- `/` – Main dashboard
- Churn Prediction – Analyze customer retention risks
- Clustering – Explore customer segments and profiles
- Satisfaction – Evaluate customer satisfaction

## ▶️ Installation & Usage

```bash
# Clone the repository
git clone YOUR_REPOSITORY_URL

# Navigate to the project
cd ProjetMLDjango

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the application
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## 🤖 Model Training

Train all three models:

```bash
python manage.py train_and_save_models
```

Train a specific model:

```bash
python manage.py train_and_save_models --model churn
python manage.py train_and_save_models --model clustering
python manage.py train_and_save_models --model satisfaction
```

## 📚 Documentation

- `GUIDE_DEPLOIEMENT_PKL.md` – Deployment guide.
- `EXPLICATION_SYSTEME_PKL.md` – Model persistence explanation.
- `OPTIMISATION_ARCHITECTURE.md` – Refactored architecture.
- `RESUME_COMPLET.md` – Complete project overview.

---

**Project Status:** Completed  
**Application:** Django + Machine Learning  
**Main Objective:** Gym Member Analytics and Customer Retention
