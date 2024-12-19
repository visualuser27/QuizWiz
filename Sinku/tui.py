import io
import json
import re
import traceback
from pdfminer.high_level import extract_text
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class PDFQuizGenerator:
    def __init__(self, model_name="google/flan-t5-base"):
        """
        Initialize the PDF Quiz Generator with a local Flan-T5 model.
        
        :param model_name: Hugging Face model name (default: google/flan-t5-base)
        """
        try:
            print("Loading model and tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            print("Model and tokenizer loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            traceback.print_exc()
    
    def extract_pdf_text(self, pdf_path):
        """
        Extract text from a PDF file
        
        :param pdf_path: Path to the PDF file
        :return: Extracted text as a string
        """
        try:
            text = extract_text(pdf_path)
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return None
    
    def generate_quiz(self, text, num_questions=5):
        """
        Generate a quiz locally using the Flan-T5 model.
        
        :param text: Text to generate quiz from
        :param num_questions: Number of quiz questions to generate
        :return: Generated quiz as a dictionary
        """
        if not text:
            return None

        # Construct the prompt
        prompt = f"""
        Generate a JSON-formatted quiz with {num_questions} multiple-choice questions based on the following text. 

        IMPORTANT INSTRUCTIONS:
        1. Respond ONLY with a valid JSON structure.
        2. Use this exact JSON format:
        {{
            "quiz_questions": [
                {{
                    "question": "Question text here",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option text here",
                    "explanation": "Explanation for the correct answer"
                }}
            ]
        }}

        Text to generate quiz from:
        {text[:2000]}  # Limit text length for better performance
        """

        try:
            # Tokenize input prompt
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

            # Generate response
            outputs = self.model.generate(**inputs, max_new_tokens=1000)

            # Decode response
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Parse JSON
            return self._parse_quiz_response(response_text)
        except Exception as e:
            print(f"Error generating quiz: {e}")
            traceback.print_exc()
            return None
    
    def _parse_quiz_response(self, response_text):
        """
        Parse the quiz response with multiple fallback methods
        
        :param response_text: Raw response text from the model
        :return: Parsed quiz dictionary or None
        """
        try:
            # Remove any markdown code block formatting
            response_text = response_text.strip('`').strip()
            
            # Try to parse as JSON
            quiz_data = json.loads(response_text)
            
            # Validate the structure
            if not isinstance(quiz_data, dict) or 'quiz_questions' not in quiz_data:
                raise ValueError("Invalid JSON structure")
            
            return quiz_data
        except (json.JSONDecodeError, ValueError) as json_error:
            print(f"JSON parsing failed: {json_error}")
            
            # Fallback: Print raw response for debugging
            print("Raw response that couldn't be parsed:")
            print(response_text)
            return None
    
    def save_quiz_to_file(self, quiz_data, output_file='quiz.json'):
        """
        Save generated quiz to a JSON file
        
        :param quiz_data: Quiz data dictionary
        :param output_file: Output file path
        """
        if quiz_data:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(quiz_data, f, indent=4, ensure_ascii=False)
                print(f"Quiz saved to {output_file}")
            except Exception as e:
                print(f"Error saving quiz: {e}")
        else:
            print("No quiz data to save.")

# Example usage
def main():
    # Path to your PDF file
    PDF_PATH = r"C:\SHRUTI'S MATERIALS\pdf-to-quizz-master\data\mod 4.pdf"
    
    try:
        # Create quiz generator
        quiz_generator = PDFQuizGenerator()
        
        # Extract text from PDF
        pdf_text = quiz_generator.extract_pdf_text(PDF_PATH)
        
        if pdf_text:
            # Generate quiz
            quiz = quiz_generator.generate_quiz(pdf_text)
            
            # Save quiz to file
            if quiz:
                quiz_generator.save_quiz_to_file(quiz)
                
                # Print quiz to console
                print(json.dumps(quiz, indent=4))
            else:
                print("Failed to generate quiz.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
