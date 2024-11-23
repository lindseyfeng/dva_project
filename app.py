import os
from artist_recommendation.cf_recommendations import ArtistRecommender
from flask import Flask, render_template, request, jsonify
from album_art_generator import make_album_art
import pandas as pd
from datetime import datetime
import spotify_artist_query as spotify
from scipy.sparse import csr_matrix, vstack
import requests


SEARCH_API_URL = "https://api.chartmetric.com/api/search"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mzk4ODkzOSwidGltZXN0YW1wIjoxNzMyMzY0NjA5NzAyLCJpYXQiOjE3MzIzNjQ2MDksImV4cCI6MTczMjM2ODIwOX0.UTpsLhDf1lPdlRGC8UM2_EjrubW2lMqwq_nuImzD_FY"
ALBUMS_API_URL = "https://api.chartmetric.com/api/artist/{artist_id}/albums"

# Headers for authorization
headers = {
    "Authorization": AUTH_TOKEN
}



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

    if request.method == 'POST':
        lyrics = request.form.get('lyrics')
        if not lyrics:
            return jsonify({'error': 'Lyrics are required to generate album art.'}), 400

        # Placeholder URL for generated album art - replace with actual generation code
        try:
            # if len(lyrics) < 10:  # Example: Check if lyrics are too short
            #     return jsonify({'error': 'Prompt too short. Please provide more details.'}), 400
            
            # Generate album art
            output_file = make_album_art(lyrics, output_file="static/images/generated_album_art.png")

            # Return the path to the generated image
            return jsonify({'image_url': f"/{output_file}"})
        except ValueError as e:
            # Handle expected errors from generate_album_art
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            print(f"Error during album art generation: {e}")
            return jsonify({'error': 'An error occurred during album art generation.'}), 500
    return render_template('album_art.html')

# Route for Music Recommendations
@app.route("/music-recommendations", methods=["GET", "POST"])
def music_recommendations():
    if request.method == "POST":
        preferences = request.form.get("preferences")
        # Placeholder recommendations - replace with actual logic
        recommendations = ["Song A", "Song B", "Song C"]
        return jsonify({"recommendations": recommendations})
    return render_template("music_recommendations.html")


@app.route('/popular-artists', methods=['GET', 'POST'])
def popular_artists():
    if request.method == 'POST':
        artist_name = request.form.get('artist_name')
        headers = {"Authorization": AUTH_TOKEN}
        
        # Fetch artist data based on the entered name
        search_response = requests.get(f"{SEARCH_API_URL}?q={artist_name}&limit=1", headers=headers)
        search_response.raise_for_status()  # Raise HTTP errors
        search_data = search_response.json().get('obj', {}).get('artists', [])
        
        if not search_data:
            print("No artists found in the search response.")
            return render_template('popular_artists.html', error="No artists found.")
        
        first_artist = search_data[0]
        first_artist_id = first_artist.get('id')
        print(f"First Artist: {first_artist['name']} (ID: {first_artist_id})")
        
        if not first_artist_id:
            print("First artist ID is missing.")
            return render_template('popular_artists.html', error="Artist ID not found.")
        
        # Render the template with artist info
        return render_template('popular_artists.html', artist=first_artist)
    else:
        # Render the form for GET requests
        return render_template('popular_artists.html')


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
