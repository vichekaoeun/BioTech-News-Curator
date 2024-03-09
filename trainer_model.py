import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def load_labeled_data(filename):
    df = pd.read_csv(filename)
    return df['Title'], df['Category']

def train_model(titles, labels):
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(titles, labels)
    return model

def classify_titles(titles, model):
    return model.predict(titles)

if __name__ == '__main__':
    titles, labels = load_labeled_data('./articles.csv')
    X_train, X_test, y_train, y_test = train_test_split(titles, labels, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    predicted_labels = classify_titles(X_test, model)
    print("Accuracy:", accuracy_score(y_test, predicted_labels))
        
    joblib.dump(model, 'trained_model.joblib')