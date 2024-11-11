from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

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
        # Placeholder URL for generated album art - replace with actual generation code
        image_url = "https://via.placeholder.com/400x400.png?text=Generated+Album+Art"
        return jsonify({'image_url': image_url})
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


# Route for Popular Artists
@app.route('/popular-artists')
def popular_artists():
    # Placeholder popular artists - replace with actual data
    popular_artists_list = ['Artist X', 'Artist Y', 'Artist Z']
    return render_template('popular_artists.html', artists=popular_artists_list)

if __name__ == '__main__':
    app.run(debug=True)
