import requests
from bs4 import BeautifulSoup

OMDB_API_KEY = 'e8746a2'  # Replace with your own OMDb API key

# Hardcoded IMDb IDs for popular series to ensure complete metadata
IMDB_ID_OVERRIDES = {
    "game of thrones": "tt0944947",
    "mirzapur": "tt6473300",
    "sacred games": "tt6077448",
    "money heist": "tt6468322",
    "breaking bad": "tt0903747"
}

def get_movie_data(title):
    # Normalize title to lowercase for mapping
    imdb_id = IMDB_ID_OVERRIDES.get(title.strip().lower())

    if imdb_id:
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    else:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    
    res = requests.get(url)
    return res.json()

def get_imdb_reviews(title):
    try:
        search_url = f"https://www.imdb.com/find?q={title.replace(' ', '+')}&s=tt"
        search_res = requests.get(search_url)
        soup = BeautifulSoup(search_res.text, "html.parser")

        # Locate the first title result and navigate to reviews
        relative_link = soup.select_one("td.result_text a")["href"]
        movie_page = f"https://www.imdb.com{relative_link}reviews"
        reviews_res = requests.get(movie_page)
        soup = BeautifulSoup(reviews_res.text, "html.parser")

        review_texts = soup.select("div.text.show-more__control")
        return [r.get_text() for r in review_texts[:10]] if review_texts else ["No reviews found."]
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return ["Could not retrieve reviews."]
