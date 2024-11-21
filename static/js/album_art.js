
// document.addEventListener('DOMContentLoaded', () => {
//     const form = document.getElementById('album-art-form');
//     form.onsubmit = async (event) => {
//         event.preventDefault();
//         const lyrics = form.lyrics.value;

//         // Show a loading message or spinner
//         document.getElementById('album-art-result').innerHTML = '<p>Generating image, please wait...</p>';

//         try {
//             const response = await fetch('/album-art', {
//                 method: 'POST',
//                 body: new URLSearchParams({ lyrics }),
//                 headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
//             });
//             const data = await response.json();

//             if (data.image_url) {
//                 // Display the image using the URL
//                 console.log(data.image_url);
//                 document.getElementById('album-art-result').innerHTML = `
//                     <h3 class="mt-4">Generated Album Art:</h3>
//                     <img src="${data.image_url}" alt="Album Art" class="img-fluid mt-3">
//                 `;
//             } else if (data.error) {
//                 document.getElementById('album-art-result').innerHTML = `<p class="text-danger">${data.error}</p>`;
//             }
//         } catch (error) {
//             console.error('Error:', error);
//             document.getElementById('album-art-result').innerHTML = '<p class="text-danger">An unexpected error occurred.</p>';
//         }
//     };
// });

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('album-art-form');
    const bufferAnimation = document.getElementById('buffer-animation');
    const albumArtContainer = document.getElementById('album-art-container');
    const albumArtResult = document.getElementById('album-art-result');

    form.onsubmit = async (event) => {
        event.preventDefault();
        const lyrics = form.lyrics.value;

        // Hide the form and show buffer animation
        form.style.display = 'none';
        bufferAnimation.style.display = 'block';

        try {
            const response = await fetch('/album-art', {
                method: 'POST',
                body: new URLSearchParams({ lyrics }),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            const data = await response.json();

            if (data.image_url) {
                // Display the image in full-screen mode
                bufferAnimation.style.display = 'none';
                albumArtResult.innerHTML = `
                    <img src="${data.image_url}" alt="Album Art" class="img-fluid mt-3">
                    <div id="action-buttons">
                        <button id="generate-new" class="btn btn-secondary">Generate New Art</button>
                        <a href="${data.image_url}" download="album_art.png" class="btn btn-success">Download Image</a>
                    </div>
                `;

                // Add event listener for "Generate New Art" button
                document.getElementById('generate-new').addEventListener('click', () => {
                    albumArtResult.innerHTML = '';
                    form.reset();
                    form.style.display = 'block';
                });
            } else if (data.error) {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            bufferAnimation.style.display = 'none';
            albumArtResult.innerHTML = `
                <p class="text-danger">An unexpected error occurred: ${error.message}</p>
                <button id="generate-new" class="btn btn-secondary">Try Again</button>
            `;

            document.getElementById('generate-new').addEventListener('click', () => {
                albumArtResult.innerHTML = '';
                form.reset();
                form.style.display = 'block';
            });
        }
    };
});
