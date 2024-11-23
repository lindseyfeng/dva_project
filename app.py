import os
from artist_recommendation.cf_recommendations import ArtistRecommender
from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
import spotify_artist_query as spotify
from scipy.sparse import csr_matrix, vstack

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


# Route to Get Recommendations (Existing)
@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    try:
        # Extract the JSON data sent from the frontend
        data = request.get_json()
        if not data or "favorite_artist" not in data:
            return jsonify({"error": "Missing 'favorite_artist' in the request"}), 400

        favorite_artist = data.get("favorite_artist").strip()
        print(f"Favorite artist: {favorite_artist}")
        if not favorite_artist:
            return jsonify({"error": "'favorite_artist' must not be empty"}), 400

        num_similar_artists = data.get("num_similar_artists")
        print(f"Number of similar artists: {num_similar_artists}")
        if not num_similar_artists:
            num_similar_artists = 10
        else:
            num_similar_artists = int(num_similar_artists)

        # Get the cluster ID for the artist
        cluster_id = recommender.get_cluster_id_for_artist(favorite_artist)
        if cluster_id == "Artist not found":
            return jsonify({"error": f"Artist '{favorite_artist}' not found"}), 404

        # Find similar artists in the same cluster
        similar_artists = recommender.get_artists_in_cluster(cluster_id)
        if not similar_artists:
            return jsonify({"error": "No similar artists found in the cluster"}), 404

        # Prepare the response data
        response = [
            {
                "name": artist,
                "image_url": spotify.get_artist_image(artist),
            }
            for artist in similar_artists[:num_similar_artists]
            if artist != favorite_artist
        ]

        # Append the favorite artist at the end
        response.append({
            "name": favorite_artist,
            "image_url": spotify.get_artist_image(favorite_artist),
        })

        return jsonify(response), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return jsonify(
            {"error": "An unexpected error occurred, please try again later"}
        ), 500


# New Route to Process Selections
@app.route("/process-selections", methods=["POST"])
def process_selections():
    try:
        # Extract the JSON data sent from the frontend
        data = request.get_json()
        print("reach here", data)
        if not data or "selected_artists" not in data:
            return jsonify({"error": "Missing 'selected_artists' in the request"}), 400

        selected_artists = data.get("selected_artists")
        print(f"Selected artists: {selected_artists}")

        if not selected_artists or not isinstance(selected_artists, list):
            return jsonify({"error": "'selected_artists' must be a non-empty list"}), 400

        filtered_artist_df = recommender.get_filtered_artist_data(selected_artists)
        cross_df = recommender.create_interaction_matrix(filtered_artist_df)

        artist_names = cross_df.columns.tolist()
        new_user_interactions = recommender.collect_user_feedback(artist_names)

        recommendations = recommender.recommend_artists(
            csr_matrix(cross_df.values), new_user_interactions, artist_names
        )

        print("Top recommended artists for you:")
        for artist in recommendations:
            print(artist)

        # Return the processed data
        return jsonify({"artists": recommendations}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred in process_selections: {e}")
        return jsonify(
            {"error": "An unexpected error occurred while processing selections"}
        ), 500


if __name__ == "__main__":
    print(os.getcwd())
    recommender = ArtistRecommender(
        artist_cluster_path="./artist_recommendation/artist_clusters.csv",
        spotify_data_path="./artist_recommendation/spotify_dataset.csv",
    )
    app.run(debug=True)
