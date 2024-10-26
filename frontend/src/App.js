import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import MusicTrends from './pages/MusicTrends';
import SimilarArtists from './pages/SimilarArtists';
import AlbumArt from './pages/AlbumArt';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Music Trends</Link> | <Link to="/similar-artists">Similar Artists</Link> | <Link to="/album-art">Album Art</Link>
      </nav>
      <Routes>
        <Route path="/" element={<MusicTrends />} />
        <Route path="/similar-artists" element={<SimilarArtists />} />
        <Route path="/album-art" element={<AlbumArt />} />
      </Routes>
    </Router>
  );
}

export default App;
