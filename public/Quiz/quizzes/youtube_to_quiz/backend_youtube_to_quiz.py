from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import openai

app = Flask(__name__)

openai.api_key = 'your-openai-api-key'

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    video_id = request.json.get('videoId')
    
    try:
        # Step 1: Extract transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript])

        # Step 2: Generate quiz using OpenAI GPT
        prompt = f"Generate multiple-choice quiz questions from the following transcript:\n\n{transcript_text}\n\nQuestions:"
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
        )

        quiz = parse_quiz(response.choices[0].text.strip())
        return jsonify({'success': True, 'quiz': quiz})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False})

def parse_quiz(generated_text):
    # This function parses the generated text into a structured quiz format.
    quiz = []
    questions = generated_text.split('\n')
    
    for question in questions:
        if question:
            parts = question.split(' - ')  # Assuming the AI separates question and options with ' - '
            question_text = parts[0]
            options = parts[1:] if len(parts) > 1 else []
            quiz.append({'text': question_text, 'options': options})
    
    return quiz

if __name__ == '__main__':
    app.run(debug=True)
