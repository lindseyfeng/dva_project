import React, { useState } from 'react';
import axios from 'axios';

const AlbumArt = () => {
  const [lyrics, setLyrics] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const generateArt = async () => {
    const response = await axios.post('http://127.0.0.1:5000/api/album-art', { lyrics });
    setImageUrl(response.data.image_url);
  };

  return (
    <div>
      <h1>Generate Custom Album Art</h1>
      <textarea value={lyrics} onChange={e => setLyrics(e.target.value)} placeholder="Enter lyrics or genres" />
      <button onClick={generateArt}>Generate Art</button>
      {imageUrl && <img src={imageUrl} alt="Album Art" />}
    </div>
  );
};

export default AlbumArt;
