from artist_recommendation.cf_recommendations import ArtistRecommender
from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)


# Mock data for demonstration purposes
mock_data = pd.DataFrame(
    {
        "artist": ["Artist A", "Artist B", "Artist C", "Artist D"],
        "streams": [5000, 6000, 7000, 8000],
        "date": ["2023-01", "2023-02", "2023-03", "2023-04"],
    }
)


# Route for Home Page
@app.route("/")
def home():
    current_year = datetime.now().year
    return render_template("index.html", current_year=current_year)


# Route for Album Art Generation
@app.route("/album-art", methods=["GET", "POST"])
def album_art():
    if request.method == "POST":
        lyrics = request.form.get("lyrics")
        # Placeholder URL for generated album art - replace with actual generation code
        image_url = "https://via.placeholder.com/400x400.png?text=Generated+Album+Art"
        return jsonify({"image_url": image_url})
    return render_template("album_art.html")


# Route for Music Recommendations
@app.route("/music-recommendations", methods=["GET", "POST"])
def music_recommendations():
    if request.method == "POST":
        preferences = request.form.get("preferences")
        # Placeholder recommendations - replace with actual logic
        recommendations = ["Song A", "Song B", "Song C"]
        return jsonify({"recommendations": recommendations})
    return render_template("music_recommendations.html")


# Route for Popular Artists
@app.route("/popular-artists")
def popular_artists():
    # Placeholder popular artists - replace with actual data
    popular_artists_list = ["Artist X", "Artist Y", "Artist Z"]
    return render_template("popular_artists.html", artists=popular_artists_list)


@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    # Extract the JSON data sent from the frontend
    data = request.get_json()
    favorite_artist = data.get("favorite_artist")  # Get the 'preferences' input

    cluster_id = recommender.get_cluster_id_for_artist(favorite_artist)
    if cluster_id == "Artist not found":
        print("Sorry, artist not found.")
        return

    # find similar artists that were grouped into the same cluster in preprocessing
    similar_artists = recommender.get_artists_in_cluster(cluster_id)
    if not similar_artists:
        print("No artists found in the cluster.")
        return
    recommendations = f"Recommendations based on your preferences: {similar_artists}"

    # Return the recommendations as a JSON response
    return jsonify({"recommendations": recommendations})


if __name__ == "__main__":
    artist_cluster_path = "/content/artist_clusters (1).csv"
    spotify_data_path = "/content/spotify_dataset.csv"

    recommender = ArtistRecommender(artist_cluster_path, spotify_data_path)
    app.run(debug=True)
