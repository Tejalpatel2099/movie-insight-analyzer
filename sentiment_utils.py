# sentiment_utils.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(reviews):
    sia = SentimentIntensityAnalyzer()
    compound_scores = [sia.polarity_scores(r)['compound'] for r in reviews]
    avg_score = sum(compound_scores) / len(compound_scores)

    if avg_score >= 0.3:
        return "Mostly Positive 😊"
    elif avg_score <= -0.3:
        return "Mostly Negative 😠"
    else:
        return "Mixed 😐"
