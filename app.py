from flask import Flask, render_template, request, jsonify
from album_art_generator import make_album_art
import pandas as pd
from datetime import datetime
import requests


SEARCH_API_URL = "https://api.chartmetric.com/api/search"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mzk4ODkzOSwidGltZXN0YW1wIjoxNzMyMTY2NjU2NjMyLCJpYXQiOjE3MzIxNjY2NTYsImV4cCI6MTczMjE3MDI1Nn0.2Q4uqVGuoEcjEQXYKk-sGPCOxmrJveoSIgfj5sZwIKY"
ALBUMS_API_URL = "https://api.chartmetric.com/api/artist/{artist_id}/albums"

# Headers for authorization
headers = {
    "Authorization": AUTH_TOKEN
}



app = Flask(__name__)

# Mock data for demonstration purposes
mock_data = pd.DataFrame({
    'artist': ['Artist A', 'Artist B', 'Artist C', 'Artist D'],
    'streams': [5000, 6000, 7000, 8000],
    'date': ['2023-01', '2023-02', '2023-03', '2023-04']
})

# Route for Home Page
@app.route('/')
def home():
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

# Route for Album Art Generation
@app.route('/album-art', methods=['GET', 'POST'])
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
@app.route('/music-recommendations', methods=['GET', 'POST'])
def music_recommendations():
    if request.method == 'POST':
        preferences = request.form.get('preferences')
        # Placeholder recommendations - replace with actual logic
        recommendations = ['Song A', 'Song B', 'Song C']
        return jsonify({'recommendations': recommendations})
    return render_template('music_recommendations.html')


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

if __name__ == '__main__':
    app.run(debug=True)
