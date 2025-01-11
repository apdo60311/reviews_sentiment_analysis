import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import opinion_lexicon
nltk.download('opinion_lexicon')

def analyze_sentiment(text):
    try:
        cleaned_text = re.sub(r'<[^>]+>|\W+|\d+', ' ', str(text)).lower()
        
        words = nltk.word_tokenize(cleaned_text)
        
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        
        processed_text = ' '.join(words)
        
        tfidf = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
        tfidf_sparse = tfidf.fit_transform([processed_text])
        
        feature_names = tfidf.get_feature_names_out()
        
        
        positive_words = set(opinion_lexicon.positive())
        negative_words = set(opinion_lexicon.negative())
        
        tfidf_array = tfidf_sparse.toarray()[0]
        positive_score = sum([tfidf_array[feature_names.tolist().index(word)] for word in positive_words if word in feature_names])
        negative_score = sum([tfidf_array[feature_names.tolist().index(word)] for word in negative_words if word in feature_names])
        
        sentiment_score = positive_score - negative_score
        total_score = positive_score + negative_score
        if sentiment_score > 0:
            return 'positive' , positive_score / total_score
        elif sentiment_score < 0:
            return 'negative', negative_score / total_score
        else:
            return 'neutral', sentiment_score / total_score
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "None", 0

def get_insights(text):
    pass