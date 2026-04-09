import pandas as pd

def get_all_movies():
    df = pd.read_csv('datasets/movies.csv')
    return df.to_dict(orient='records')

def get_mood_recommendations(mood):
    df = pd.read_csv('datasets/movies.csv')
    # Filter by mood
    recs = df[df['mood'].str.lower() == mood.lower()]
    if recs.empty:
        return df.head(3).to_dict(orient='records') # Fallback
    return recs.to_dict(orient='records')

def search_movies(query):
    df = pd.read_csv('datasets/movies.csv')
    # Case insensitive search in titles
    results = df[df['title'].str.contains(query, case=False)]
    return results.to_dict(orient='records')