document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('similar-artists-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        const artist = form.artist.value;
        const response = await fetch('/similar-artists', {
            method: 'POST',
            body: new URLSearchParams({ artist }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        const data = await response.json();
        document.getElementById('similar-artists-list').innerHTML = data.similar_artists.map(artist => `<li>${artist}</li>`).join('');
    };
});
