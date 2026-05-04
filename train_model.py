import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("spam.csv", encoding="latin-1")
df = df[['sms', 'label']]

df = df.dropna()
df['sms'] = df['sms'].astype(str)

X = df['sms']
y = df['label']

vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=2000)
model.fit(X_vec, y)

pickle.dump(model, open("spam_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print(" Model trained")