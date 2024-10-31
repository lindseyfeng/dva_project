document.addEventListener('DOMContentLoaded', () => {
    const trendsForm = document.getElementById('trends-form');
    trendsForm.onsubmit = async (event) => {
        event.preventDefault();
        const artist = trendsForm.artist.value;
        const response = await fetch('/music-trends', {
            method: 'POST',
            body: new URLSearchParams({ artist }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        const data = await response.json();
        document.getElementById('chart-container').innerText = JSON.stringify(data, null, 2);
    };
});
