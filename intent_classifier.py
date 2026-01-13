import json
import random
import nltk

#nltk.download('punkt')
#nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

STOPWORDS = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalpha() and w not in STOPWORDS]
    return " ".join(tokens)

INTENTS_PATH = r"C:\Users\kittu\Desktop\personal_ai_assistant\intents.json"

with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


corpus = []
labels = []
responses = {}

for intent in data["intents"]:
    tag = intent["tag"]
    responses[tag] = intent["responses"]
    for pattern in intent["patterns"]:
        corpus.append(preprocess(pattern))
        labels.append(tag)

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

# Train model
model = LogisticRegression()
model.fit(X, labels)

def predict_intent(text):
    text_p = preprocess(text)
    X_test = vectorizer.transform([text_p])

    probs = model.predict_proba(X_test)[0]
    max_prob = probs.max()
    tag = model.classes_[probs.argmax()]

    # 🔥 Confidence threshold
    if max_prob < 0.20:
        return "fallback", "I’m not fully sure what you mean. Can you rephrase?"

    return tag, random.choice(responses[tag])


# Testing
if __name__ == "__main__":
    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            break
        intent, reply = predict_intent(msg)
        print(f"Intent: {intent}")
        print(f"Bot: {reply}")
