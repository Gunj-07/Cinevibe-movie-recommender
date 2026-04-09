from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download sentiment lexicon quietly
nltk.download('vader_lexicon', quiet=True)

app = Flask(__name__)

def get_categorized_movies():
    """Fetches movies from the dataset and categorizes them for the UI."""
    try:
        df = pd.read_csv('datasets/movies.csv')
        movies = df.to_dict(orient='records')
        return {
            'all': movies,
            'trending': random.sample(movies, 10) if len(movies) >= 10 else movies,
            'bollywood': [m for m in movies if 'Hindi' in m['language']][:10],
            'action': [m for m in movies if 'Action' in m['genres']][:10],
            'scifi': [m for m in movies if 'Sci-Fi' in m['genres']][:10],
            'comedy': [m for m in movies if 'Comedy' in m['genres']][:10]
        }
    except Exception as e:
        print(f"Error loading movies: {e}")
        return {'all': [], 'trending': [], 'bollywood': [], 'action': [], 'scifi': [], 'comedy': []}

@app.route('/')
def home():
    categories = get_categorized_movies()
    return render_template('index.html', categories=categories)

@app.route('/api/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower()
    df = pd.read_csv('datasets/movies.csv')
    results = df[df['title'].str.lower().str.contains(query)]
    return jsonify({'movies': results.to_dict(orient='records')})

@app.route('/api/mood', methods=['POST'])
def mood_match():
    mood = request.json.get('mood', 'Happy')
    df = pd.read_csv('datasets/movies.csv')
    recs = df[df['mood'].str.lower() == mood.lower()]
    return jsonify({'movies': recs.to_dict(orient='records')})

# --- ADVANCED SENTIMENT ENGINE (RATING FLUCTUATION) ---
@app.route('/api/analyze_review', methods=['POST'])
def analyze_review():
    data = request.json
    review = data.get('review', '')
    base_rating = float(data.get('base_rating', 4.5))
    
    # Initialize NLP Analyzer
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(review)
    compound = score['compound'] # Ranges from -1 (Negative) to 1 (Positive)
    
    # Fluctuate the rating mathematically based on emotion intensity
    # Max change is +/- 0.5 stars
    change = compound * 0.5
    new_rating = round(base_rating + change, 1)
    new_rating = min(max(new_rating, 1.0), 5.0) # Keep it between 1 and 5
    
    if compound > 0.05:
        sentiment = "Positive 📈"
        color = "text-emerald-400" # Updated theme color to Emerald
    elif compound < -0.05:
        sentiment = "Negative 📉"
        color = "text-red-400"
    else:
        sentiment = "Neutral ➖"
        color = "text-gray-400"
        
    return jsonify({
        'new_rating': new_rating, 
        'sentiment': sentiment, 
        'color': color,
        'change': round(change, 2)
    })

# --- CHATBOT ENGINE (VibeMind AI) ---
@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').lower()
    df = pd.read_csv('datasets/movies.csv')
    
    # Rebranded Greeting
    if user_msg in ['hi', 'hello', 'hey']:
        return jsonify({'reply': "Hello! ✨ I am VibeMind AI. Describe a story, plot, or genre you want to watch!"})
    
    try:
        # ML Logic for recommendation via text similarity
        df['combined_features'] = df['genres'] + " " + df['description'] + " " + df['title']
        all_text = df['combined_features'].tolist()
        all_text.append(user_msg)
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_text)
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        
        # Get top 2 matches
        top_indices = cosine_sim.argsort()[-2:][::-1]
        
        if cosine_sim[top_indices[0]] > 0.05:
            top_movies = df.iloc[top_indices]['title'].tolist()
            reply = f"Based on my AI analysis, I highly recommend: **{', '.join(top_movies)}**. 🎬"
        else:
            reply = "I couldn't find an exact plot match in our database. Try typing a genre like 'Action' or 'Sci-Fi'!"
    except Exception as e:
        reply = "I encountered an error processing that. Please try asking for a specific genre or mood!"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    # Ensure the dataset folder exists if running for the first time
    import os
    if not os.path.exists('datasets/movies.csv'):
        print("Warning: datasets/movies.csv not found. Please run your data generation script first.")
        
    app.run(debug=True)