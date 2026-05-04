# Spam Email Detection Web App 

A full-stack web application that classifies emails as Spam or Not Spam using Machine Learning. The system includes user authentication, prediction history, analytics dashboard, and a demo premium upgrade system.

---

# Key Features

-  User Registration & Login system
-  Spam Detection using Machine Learning
-  Dashboard with analytics and usage tracking
-  Prediction History stored in database
-  Demo Razorpay Payment Integration (UI only)
-  Premium Upgrade Feature

---

## Machine Learning Pipeline

1. User inputs email text  
2. Text preprocessing:
   - Lowercasing
   - Removing stopwords
   - Cleaning text  
3. Feature extraction using TF-IDF / CountVectorizer  
4. Model prediction using trained ML model  
5. Result displayed and stored in database  

---

##  Model Details

- Algorithm: Naive Bayes / Logistic Regression *(update this)*
- Vectorizer: TF-IDF / CountVectorizer *(update this)*

---

## Model Performance

- Accuracy: 95% *(update this)*  
- Reliable spam classification with good precision and recall  

---

## 🛠 Tech Stack

**Backend:**
- Python (Flask)
- SQLite Database

**Machine Learning:**
- Scikit-learn
- Pandas / NumPy

**Frontend:**
- HTML, CSS, JavaScript

---

##  Screenshots

_Add screenshots of your application_

```md
## 📸 Screenshots

![Login Page](images/login.png)
![Spam Prediction](images/predict.png)
![Dashboard](images/dashboard.png)
