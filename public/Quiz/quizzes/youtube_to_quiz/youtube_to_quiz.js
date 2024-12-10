document.getElementById('process-video').addEventListener('click', async function () {
    const youtubeUrl = document.getElementById('youtube-url').value;

    if (youtubeUrl) {
        try {
            // Send a POST request to the backend to process the video
            const response = await fetch('/process-video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: youtubeUrl }),  // Sending URL in the request body
            });

            const data = await response.json();

            // Handle the response
            alert(data.message);  // Show message from backend

            // Display the next section (for example, the quiz)
            document.getElementById('quiz-section').style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to process video.');
        }
    } else {
        alert('Please enter a YouTube URL.');
    }
});
