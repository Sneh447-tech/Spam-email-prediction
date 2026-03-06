#  Spam Email Detection using Machine Learning

## Project Overview

Spam emails are unwanted messages that may contain advertisements, phishing links, or malicious content. Detecting spam emails automatically is important to keep inboxes safe and organized.

This project uses **Machine Learning techniques** to classify emails as **Spam** or **Not Spam (Ham)**. The model is trained on a labeled dataset of emails and learns patterns in spam messages such as suspicious words, links, and unusual text structures.

The goal of this project is to build a **simple and efficient spam detection system** that can automatically filter unwanted emails.

---

## Objectives

* To understand the working of **machine learning in text classification**
* To preprocess email text data
* To train a model that can classify emails into spam or ham
* To evaluate the accuracy of the spam detection system

---

##  Technologies Used

* **Python**
* **Machine Learning**
* **Scikit-learn**
* **Pandas**
* **NumPy**
* **Natural Language Processing (NLP)**

---

##  Project Workflow

1 **Data Collection**
The dataset containing labeled emails (spam/ham) is collected.

2 **Data Preprocessing**

* Removing stop words
* Lowercasing text
* Removing punctuation
* Tokenization

3 **Feature Extraction**
Text data is converted into numerical form using techniques like:

* **Bag of Words**
* **TF-IDF Vectorization**

4 **Model Training**
Machine learning algorithms such as:

* Naive Bayes
* Logistic Regression
* Support Vector Machine (optional)

5 **Model Evaluation**
The model is evaluated using:

* Accuracy
* Confusion Matrix
* Precision and Recall

---

## Project Structure

```
spam-email-detection
│
├── dataset
│   └── spam.csv
│
├── notebook
│   └── spam_detection.ipynb
│
├── model
│   └── spam_model.pkl
│
├── src
│   └── train_model.py
│
├── requirements.txt
│
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/spam-email-detection.git
```

Move to the project directory

```bash
cd spam-email-detection
```

Install required libraries

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the training script

```bash
python train_model.py
```

Or open the Jupyter notebook

```bash
jupyter notebook
```

---

## Example Output

Input Email:

```
Congratulations! You have won a free lottery ticket.
Click here to claim your prize.
```

Prediction:

```
Spam
```

---

