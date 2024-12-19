from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader
from transformers import pipeline

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit: 16MB

# Load the Hugging Face question-generation pipeline
question_generator = pipeline('text2text-generation', model="valhalla/t5-small-qg-prepend")

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# API endpoint for quiz generation
@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file securely
    filename = secure_filename(pdf_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(file_path)

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(file_path)
    if not pdf_text:
        return jsonify({'error': 'Unable to extract text from PDF'}), 500

    # Limit text to the first 1000 characters for processing
    pdf_text = pdf_text[:1000]  # You can adjust this limit based on your needs

    # Generate questions using the AI model
    try:
        questions = question_generator(pdf_text)
        quiz = [{"question": q['generated_text']} for q in questions]
        return jsonify({'quiz': quiz})
    except Exception as e:
        print(f"Error generating questions: {e}")
        return jsonify({'error': 'Question generation failed'}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
