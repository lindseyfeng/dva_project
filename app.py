import os
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
    try:
        # Extract the JSON data sent from the frontend
        data = request.get_json()
        if not data or "favorite_artist" not in data:
            return jsonify({"error": "Missing 'favorite_artist' in the request"}), 400

        favorite_artist = data.get("favorite_artist").strip()
        print(favorite_artist)
        if not favorite_artist:
            return jsonify({"error": "'favorite_artist' must not be empty"}), 400

        # Get the cluster ID for the artist
        cluster_id = recommender.get_cluster_id_for_artist(favorite_artist)
        if cluster_id == "Artist not found":
            return jsonify({"error": f"Artist '{favorite_artist}' not found"}), 404

        # Find similar artists in the same cluster
        similar_artists = recommender.get_artists_in_cluster(cluster_id)
        if not similar_artists:
            return jsonify({"error": "No similar artists found in the cluster"}), 404

        # Create recommendations
        recommendations = (
            f"Recommendations based on your preferences: {similar_artists}"
        )
        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return jsonify(
            {"error": "An unexpected error occurred, please try again later"}
        ), 500


if __name__ == "__main__":
    print(os.getcwd())
    recommender = ArtistRecommender(
        artist_cluster_path="artist_clusters.csv",
        spotify_data_path="spotify_dataset.csv",
    )
    app.run(debug=True)
