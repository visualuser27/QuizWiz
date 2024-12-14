// File upload event listener
document.getElementById('pdf-upload').addEventListener('change', function(e) {
    const fileName = e.target.files[0] ? e.target.files[0].name : 'No file selected';
    document.getElementById('file-name').textContent = fileName;

    // Show the "Change File" and "Generate Quiz" buttons after selecting a file
    document.getElementById('change-file').style.display = 'inline-block'; // Show Change File button
    document.getElementById('generate-quiz').style.display = 'inline-block'; // Show Generate Quiz button

    // Enable the Generate Quiz button if a file is selected
    document.getElementById('generate-quiz').disabled = !e.target.files.length;
});

// Change file functionality
document.getElementById('change-file').addEventListener('click', function() {
    document.getElementById('pdf-upload').value = ''; // Reset file input
    document.getElementById('file-name').textContent = 'No file selected'; // Reset file name
    document.getElementById('change-file').style.display = 'none'; // Hide "Change File" button
    document.getElementById('generate-quiz').style.display = 'none'; // Hide "Generate Quiz" button

    // Disable the Generate Quiz button until a new file is selected
    document.getElementById('generate-quiz').disabled = true;
});

// Handling Generate Quiz Button click
document.getElementById('generate-quiz').addEventListener('click', function() {
    // Logic to send the PDF to the backend for quiz generation
    alert('Quiz generation in progress...');
});
// Handling Generate Quiz Button click
document.getElementById('generate-quiz').addEventListener('click', function() {
    const fileInput = document.getElementById('pdf-upload');
    const file = fileInput.files[0];
    
    if (file) {
        const formData = new FormData();
        formData.append('pdf', file);
        
        // Make a POST request to the backend to process the PDF and generate the quiz
        fetch('/generate-quiz', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.quiz) {
                // Display quiz (e.g., show quiz questions and options)
                displayQuiz(data.quiz);
            } else {
                alert('Error generating quiz');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

// Function to display the generated quiz (for example, as a list of questions)
function displayQuiz(quiz) {
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = '';  // Clear previous quiz content

    quiz.questions.forEach((question, index) => {
        const questionElement = document.createElement('div');
        questionElement.innerHTML = `
            <h3>${index + 1}. ${question.question}</h3>
            <ul>
                ${question.options.map(option => `<li>${option}</li>`).join('')}
            </ul>
        `;
        quizContainer.appendChild(questionElement);
    });
}
