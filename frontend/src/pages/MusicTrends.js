import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

const MusicTrends = () => {
  const [artist, setArtist] = useState('');
  const [data, setData] = useState(null);

  const fetchTrends = async () => {
    const response = await axios.get(`http://127.0.0.1:5000/api/music-trends?artist=${artist}`);
    setData(response.data);
  };

  const chartData = {
    labels: data?.map(entry => entry.date),
    datasets: [
      {
        label: `Streams for ${artist}`,
        data: data?.map(entry => entry.streams),
        borderWidth: 2,
      },
    ],
  };

  return (
    <div>
      <h1>Music Trends</h1>
      <input type="text" value={artist} onChange={e => setArtist(e.target.value)} placeholder="Enter artist name" />
      <button onClick={fetchTrends}>Fetch Trends</button>
      {data && <Line data={chartData} />}
    </div>
  );
};

export default MusicTrends;
