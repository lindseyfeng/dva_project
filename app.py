import os
from artist_recommendation.cf_recommendations import ArtistRecommender
from flask import Flask, render_template, request, jsonify
from album_art_generator import make_album_art
import pandas as pd
from datetime import datetime
import spotify_artist_query as spotify
from scipy.sparse import csr_matrix, vstack
import requests
from pytrends.request import TrendReq
import json
import ast
import csv
import io


SEARCH_API_URL = "https://api.chartmetric.com/api/search"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mzk4ODkzOSwidGltZXN0YW1wIjoxNzMyNDEwMzkwNjk3LCJpYXQiOjE3MzI0MTAzOTAsImV4cCI6MTczMjQxMzk5MH0.-LLgmVj05hd7zTdw07qyowYyM0y78kdw6IoB1jnhaik"
ALBUMS_API_URL = "https://api.chartmetric.com/api/artist/{artist_id}/albums"

# Headers for authorization
headers = {"Authorization": AUTH_TOKEN}


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
        if not lyrics:
            return jsonify({"error": "Lyrics are required to generate album art."}), 400

        # Placeholder URL for generated album art - replace with actual generation code
        try:
            # if len(lyrics) < 10:  # Example: Check if lyrics are too short
            #     return jsonify({'error': 'Prompt too short. Please provide more details.'}), 400

            # Generate album art
            output_file = make_album_art(
                lyrics, output_file="static/images/generated_album_art.png"
            )

            # Return the path to the generated image
            return jsonify({"image_url": f"/{output_file}"})
        except ValueError as e:
            # Handle expected errors from generate_album_art
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Error during album art generation: {e}")
            return jsonify(
                {"error": "An error occurred during album art generation."}
            ), 500
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


# @app.route('/popular-artists', methods=['GET', 'POST'])
# def popular_artists():
#     if request.method == 'POST':
#         artist_name = request.form.get('artist_name')
#         headers = {"Authorization": AUTH_TOKEN}

#         # # Fetch artist data based on the entered name
#         # search_response = requests.get(f"{SEARCH_API_URL}?q={artist_name}&limit=1", headers=headers)
#         # search_response.raise_for_status()  # Raise HTTP errors
#         # search_data = search_response.json().get('obj', {}).get('artists', [])

#         # if not search_data:
#         #     print("No artists found in the search response.")
#         #     return render_template('popular_artists.html', error="No artists found.")

#         # first_artist = search_data[0]
#         # first_artist_id = first_artist.get('id')
#         # print(f"First Artist: {first_artist['name']} (ID: {first_artist_id})")

#         # if not first_artist_id:
#         #     print("First artist ID is missing.")
#         #     return render_template('popular_artists.html', error="Artist ID not found.")

#         # Render the template with artist info
#         # try:
#         #     pytrends = TrendReq(hl='en-US', tz=360)
#         #     kw_list = [artist_name]
#         #     pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
#         #     trends_data = pytrends.interest_over_time()
#         #     if not trends_data.empty:
#         #         # Reset index to convert the date index into a column
#         #         trends_data = trends_data.reset_index()
#         #         # Convert DataFrame to a list of dictionaries for easy use in templates
#         #         trends_data_list = trends_data.to_dict(orient='records')
#         #     else:
#         #         print("No Google Trends data found.")
#         #         trends_data_list = []
#         # except Exception as e:
#         #     print(f"Error fetching Google Trends data: {e}")
#         #     trends_data_list = []
#         # print("reach here")
#         # print(trends_data_list)

#         trends_data_list = "[{'date': Timestamp('2023-11-19 00:00:00'), 'Taylor Swift': 46, 'isPartial': False}, {'date': Timestamp('2023-11-20 00:00:00'), 'Taylor Swift': 50, 'isPartial': False}]"

#         # Step 1: Replace `Timestamp` with a simple representation
#         trends_data_list = trends_data_list.replace("Timestamp('", '"').replace("')", '"')
#         trends_data_list = trends_data_list.replace("'", '"')
#         print(trends_data_list)
#         # Step 2: Use `ast.literal_eval` to safely evaluate the string as a Python object
#         data = ast.literal_eval(trends_data_list)
#         print(data)
#         for entry in data:
#             entry['date'] = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')

#         # Step 2: Extract the date and "Taylor Swift" value
#         csv_data = [(entry['date'].strftime('%Y-%m-%d'), entry['Taylor Swift']) for entry in data]

#         # Step 3: Save to CSV string
#         csv_output = io.StringIO()
#         writer = csv.writer(csv_output)
#         writer.writerow(['date', f'test'])  # Write header
#         writer.writerows(csv_data)  # Write data

#         # Retrieve the CSV string
#         csv_variable = csv_output.getvalue()
#         csv_output.close()
#         #print(csv_variable)
#         df = pd.read_csv(io.StringIO(csv_variable))
#         json_data = df.to_json(orient='records')
#         print(json_data)
#         first_artist = {}
#         first_artist['name'] = "test"
#         first_artist['id'] = 123
#         return render_template('popular_artists.html', artist=first_artist, trends_data=json_data)
#     else:
#         # Render the form for GET requests
#         return render_template('popular_artists.html')


@app.route("/popular-artists", methods=["GET", "POST"])
def popular_artists():
    if request.method == "POST":
        artist_name = request.form.get("artist_name")
        headers = {"Authorization": AUTH_TOKEN}

        # # Fetch artist data based on the entered name
        search_response = requests.get(
            f"{SEARCH_API_URL}?q={artist_name}&limit=1", headers=headers
        )
        search_response.raise_for_status()  # Raise HTTP errors
        search_data = search_response.json().get("obj", {}).get("artists", [])

        if not search_data:
            print("No artists found in the search response.")
            return render_template("popular_artists.html", error="No artists found.")

        first_artist = search_data[0]
        first_artist_id = first_artist.get("id")
        print(f"First Artist: {first_artist['name']} (ID: {first_artist_id})")

        if not first_artist_id:
            print("First artist ID is missing.")
            return render_template("popular_artists.html", error="Artist ID not found.")

        # Sample data (replace with your actual data fetching logic)
        data = [
            {"date": "2023-11-19", "Taylor Swift": 46},
            {"date": "2023-10-20", "Taylor Swift": 40},
            {"date": "2023-09-20", "Taylor Swift": 60},
            {"date": "2023-08-20", "Taylor Swift": 57},
            {"date": "2023-07-20", "Taylor Swift": 57},
            {"date": "2023-06-20", "Taylor Swift": 57},
            {"date": "2023-05-20", "Taylor Swift": 53},
            {"date": "2023-04-20", "Taylor Swift": 56},
            {"date": "2023-03-20", "Taylor Swift": 70},
            {"date": "2023-02-20", "Taylor Swift": 40},
            {"date": "2023-01-20", "Taylor Swift": 50},
            {"date": "2022-12-20", "Taylor Swift": 60},
        ]

        # Create artist info with the exact same name as in the data
        return render_template(
            "popular_artists.html", artist=first_artist, trends_data=data
        )
    else:
        return render_template("popular_artists.html")


@app.route("/popular-artist-info", methods=["GET", "POST"])
def popular_artist_info():
    try:
        # Extract the JSON data sent from the frontend
        data = request.get_json()
        if not data or "artist_name" not in data:
            return jsonify({"error": "Missing 'artist_name' in the request"}), 400

        artist_name = data.get("artist_name").strip()
        print("Artist name for popular info: ", artist_name)
        print(f"Favorite artist: {artist_name}")
        if not artist_name:
            return jsonify({"error": "'favorite_artist' must not be empty"}), 400

        # Prepare the response data
        response = [
            {
                "image_url": spotify.get_artist_image(artist_name),
                "dates": [],
                "values": 
                "artist_data":  # Sample data (replace with your actual data fetching logic)
                [
                    {"date": "2023-11-19", "Taylor Swift": 46},
                    {"date": "2023-10-20", "Taylor Swift": 40},
                    {"date": "2023-09-20", "Taylor Swift": 60},
                    {"date": "2023-08-20", "Taylor Swift": 57},
                    {"date": "2023-07-20", "Taylor Swift": 57},
                    {"date": "2023-06-20", "Taylor Swift": 57},
                    {"date": "2023-05-20", "Taylor Swift": 53},
                    {"date": "2023-04-20", "Taylor Swift": 56},
                    {"date": "2023-03-20", "Taylor Swift": 70},
                    {"date": "2023-02-20", "Taylor Swift": 40},
                    {"date": "2023-01-20", "Taylor Swift": 50},
                    {"date": "2022-12-20", "Taylor Swift": 60},
                ],
            }
        ]

        return jsonify(response), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return jsonify(
            {"error": "An unexpected error occurred, please try again later"}
        ), 500


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
        response.append(
            {
                "name": favorite_artist,
                "image_url": spotify.get_artist_image(favorite_artist),
            }
        )

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
            return jsonify(
                {"error": "'selected_artists' must be a non-empty list"}
            ), 400

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
    # recommender = ArtistRecommender(
    #     artist_cluster_path="./artist_recommendation/artist_clusters.csv",
    #     spotify_data_path="./artist_recommendation/spotify_dataset.csv",
    # )
    app.run(debug=True)
