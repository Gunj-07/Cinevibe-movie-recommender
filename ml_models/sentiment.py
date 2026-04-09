import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download lexicon on first run
nltk.download('vader_lexicon', quiet=True)

def analyze_review_sentiment(review_text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(review_text)
    
    if score['compound'] >= 0.05:
        return "Positive Audience Sentiment 📈"
    elif score['compound'] <= -0.05:
        return "Negative Audience Sentiment 📉"
    else:
        return "Neutral Audience Sentiment ➖"