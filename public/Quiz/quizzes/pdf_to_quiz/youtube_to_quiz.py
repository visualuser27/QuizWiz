from flask import Flask, request, jsonify
import PyPDF2

app = Flask(__name__)

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    # Get the uploaded file
    pdf_file = request.files.get('pdf')

    if not pdf_file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Extract text from the PDF
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Generate a simple quiz from the text (just as an example)
    quiz = generate_quiz_from_text(text)

    return jsonify({'quiz': quiz})

def generate_quiz_from_text(text):
    # Simple example: split text into questions and generate MCQs
    questions = []    
    # A very basic method to extract questions (this could be much more complex)
    paragraphs = text.split('\n')
    for para in paragraphs:
        if '?' in para:  # Simple check for a question
            question = {
                'question': para,
                'options': ['Option A', 'Option B', 'Option C', 'Option D']  # Dummy options
            }
            questions.append(question)
    
    return {'questions': questions}

if __name__ == '__main__':
    app.run(debug=True)
