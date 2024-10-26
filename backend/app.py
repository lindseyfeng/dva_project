from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import album_art

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Mock data for music trends
mock_data = pd.DataFrame({
    'artist': ['Artist A', 'Artist B', 'Artist A', 'Artist C'],
    'streams': [5000, 6000, 7000, 8000],
    'date': ['2023-01', '2023-02', '2023-03', '2023-04']
})

@app.route('/api/music-trends', methods=['GET'])
def get_music_trends():
    artist = request.args.get('artist')
    artist_data = mock_data[mock_data['artist'] == artist]
    return artist_data.to_json(orient='records')

@app.route('/api/similar-artists', methods=['POST'])
def find_similar_artists():
    data = request.json
    # Placeholder: Replace this with your ML model logic
    user_input = data.get('artist')
    similar_artists = ['Artist B', 'Artist C']  # Example result
    return jsonify({'similar_artists': similar_artists})

@app.route('/api/album-art', methods=['POST'])
def generate_album_art():
    lyrics = request.json.get('lyrics')
    image_url = album_art.generate_image(lyrics)
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=True)
