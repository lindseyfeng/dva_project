
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('album-art-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        const lyrics = form.lyrics.value;

        // Show a loading message or spinner
        document.getElementById('album-art-result').innerHTML = '<p>Generating image, please wait...</p>';

        try {
            const response = await fetch('/album-art', {
                method: 'POST',
                body: new URLSearchParams({ lyrics }),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            const data = await response.json();

            if (data.image_url) {
                // Display the image using the URL
                console.log(data.image_url);
                document.getElementById('album-art-result').innerHTML = `
                    <h3 class="mt-4">Generated Album Art:</h3>
                    <img src="${data.image_url}" alt="Album Art" class="img-fluid mt-3">
                `;
            } else if (data.error) {
                document.getElementById('album-art-result').innerHTML = `<p class="text-danger">${data.error}</p>`;
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('album-art-result').innerHTML = '<p class="text-danger">An unexpected error occurred.</p>';
        }
    };
});