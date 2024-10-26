import React, { useState } from 'react';
import axios from 'axios';

const SimilarArtists = () => {
  const [artist, setArtist] = useState('');
  const [similarArtists, setSimilarArtists] = useState([]);

  const findSimilar = async () => {
    const response = await axios.post('http://127.0.0.1:5000/api/similar-artists', { artist });
    setSimilarArtists(response.data.similar_artists);
  };

  return (
    <div>
      <h1>Discover Similar Artists</h1>
      <input type="text" value={artist} onChange={e => setArtist(e.target.value)} placeholder="Enter artist name" />
      <button onClick={findSimilar}>Find Similar Artists</button>
      <ul>
        {similarArtists.map((artist, index) => (
          <li key={index}>{artist}</li>
        ))}
      </ul>
    </div>
  );
};

export default SimilarArtists;
