document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('album-art-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        const lyrics = form.lyrics.value;
        const response = await fetch('/album-art', {
            method: 'POST',
            body: new URLSearchParams({ lyrics }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        const data = await response.json();
        document.getElementById('album-art-result').innerHTML = `<img src="${data.image_url}" alt="Album Art">`;
    };
});
