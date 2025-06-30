from flask import Flask, render_template, request
from movie_utils import get_movie_data, get_imdb_reviews
from sentiment_utils import analyze_sentiment
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


app = Flask(__name__)

# Helper function to extract Rotten Tomatoes score
def get_rotten_tomatoes_rating(data):
    for rating in data.get("Ratings", []):
        if rating["Source"] == "Rotten Tomatoes":
            return rating["Value"]
    return "N/A"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["movie"]
        print(f"🎬 User input movie: {title}")

        # Get metadata from OMDb
        movie_data = get_movie_data(title)
        if movie_data.get("Response") == "False":
            return render_template("index.html", error="Movie or series not found. Please try another title.")

        # Get sentiment and additional metadata
        reviews = get_imdb_reviews(title)
        sentiment = analyze_sentiment(reviews)
        genre = movie_data.get("Genre", "N/A")
        tomatoes = get_rotten_tomatoes_rating(movie_data)
        director = movie_data.get("Director", "N/A")
        actors = movie_data.get("Actors", "N/A")
        released = movie_data.get("Released", "N/A")
        runtime = movie_data.get("Runtime", "N/A")
        poster = movie_data.get("Poster", "")
        type_ = movie_data.get("Type", "N/A").title()
        total_seasons = movie_data.get("totalSeasons", None)

        print(f"✅ Type: {type_}, Genre: {genre}, 🍅 Rotten Tomatoes: {tomatoes}, 🧠 Sentiment: {sentiment}")

        return render_template("index.html",
                               title=movie_data.get("Title", "N/A"),
                               plot=movie_data.get("Plot", "N/A"),
                               rating=movie_data.get("imdbRating", "N/A"),
                               sentiment=sentiment,
                               genre=genre,
                               tomatoes=tomatoes,
                               director=director,
                               actors=actors,
                               released=released,
                               runtime=runtime,
                               type_=type_,
                               total_seasons=total_seasons,
                               poster=poster)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)