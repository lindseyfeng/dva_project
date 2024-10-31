from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Mock data for demonstration
mock_data = pd.DataFrame({
    'artist': ['Artist A', 'Artist B', 'Artist A', 'Artist C'],
    'streams': [5000, 6000, 7000, 8000],
    'date': ['2023-01', '2023-02', '2023-03', '2023-04']
})

# Homepage route
@app.route('/')
def home():
    return render_template('base.html')

# Route for Music Trends
@app.route('/music-trends', methods=['GET', 'POST'])
def music_trends():
    if request.method == 'POST':
        artist = request.form.get('artist')
        artist_data = mock_data[mock_data['artist'] == artist]
        return jsonify(artist_data.to_dict(orient='records'))
    return render_template('music_trends.html')

# Route for Similar Artists
@app.route('/similar-artists', methods=['GET', 'POST'])
def similar_artists():
    if request.method == 'POST':
        artist = request.form.get('artist')
        # Placeholder similar artists - replace with ML logic
        similar_artists = ['Artist B', 'Artist C']
        return jsonify({'similar_artists': similar_artists})
    return render_template('similar_artists.html')

# Route for Album Art Generation
@app.route('/album-art', methods=['GET', 'POST'])
def album_art():
    if request.method == 'POST':
        lyrics = request.form.get('lyrics')
        # Placeholder URL for generated album art - replace with actual generation code
        image_url = "https://example.com/generated-album-art.png"
        return jsonify({'image_url': image_url})
    return render_template('album_art.html')

if __name__ == '__main__':
    app.run(debug=True)
