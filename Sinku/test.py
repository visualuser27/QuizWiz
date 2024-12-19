import io
import json
from pdfminer.high_level import extract_text
from huggingface_hub import InferenceClient

class PDFQuizGenerator:
    def __init__(self, hf_api_key):
        """
        Initialize the PDF Quiz Generator
        
        :param hf_api_key: Hugging Face API key
        """
        self.hf_client = InferenceClient(api_key=hf_api_key)
    
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
        Generate a quiz from the extracted text using Qwen
        
        :param text: Text to generate quiz from
        :param num_questions: Number of quiz questions to generate
        :return: Generated quiz as a dictionary
        """
        if not text:
            return None
        
        # Prompt to generate a quiz
        prompt = f"""Based on the following text, create a comprehensive quiz with {num_questions} questions. 
        Each question should:
        - Have 4 multiple-choice options
        - Include the correct answer
        - Cover different aspects of the text
        - Vary in difficulty

        Text to generate quiz from:
        {text[:4000]}  # Limit text to prevent overwhelming the model

        Format the response as a JSON with this structure:
        {{
            "quiz_questions": [
                {{
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "Correct Option Letter",
                    "explanation": "Brief explanation of the correct answer"
                }}
            ]
        }}
        """
        
        try:
            # Send request to Qwen
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            completion = self.hf_client.chat.completions.create(
                model="Qwen/Qwen2.5-0.5B", 
                messages=messages, 
                max_tokens=1000
            )
            
            # Extract and parse the response
            response_text = completion.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                quiz_data = json.loads(response_text)
                return quiz_data
            except json.JSONDecodeError:
                print("Failed to parse quiz JSON. Attempting to extract manually.")
                # Fallback parsing if JSON is malformed
                return self._parse_quiz_manually(response_text)
        
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return None
    
    def _parse_quiz_manually(self, response_text):
        """
        Manually parse quiz if JSON parsing fails
        
        :param response_text: Raw response text
        :return: Parsed quiz dictionary or None
        """
        # Implement basic manual parsing logic
        # This is a simplified approach and may not work for all responses
        try:
            # Look for JSON-like patterns
            quiz_data = {
                "quiz_questions": []
            }
            
            # Basic parsing logic (very rudimentary)
            import re
            
            # Extract questions using regex
            question_matches = re.findall(r'(\d+\.\s*.*?)\n(A\.\s*.*?)\n(B\.\s*.*?)\n(C\.\s*.*?)\n(D\.\s*.*?)\n', response_text, re.DOTALL)
            
            for match in question_matches:
                question = match[0].strip()
                options = [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()]
                
                quiz_data["quiz_questions"].append({
                    "question": question,
                    "options": options,
                    "correct_answer": "A",  # Default, would need more sophisticated parsing
                    "explanation": ""
                })
            
            return quiz_data if quiz_data["quiz_questions"] else None
        
        except Exception as e:
            print(f"Manual parsing failed: {e}")
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
    # Replace with your actual Hugging Face API key
    HF_API_KEY = "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"
    PDF_PATH = "C:\\SHRUTI'S MATERIALS\\pdf-to-quizz-master\\data\\mod 4.pdf"
    
    # Create quiz generator
    quiz_generator = PDFQuizGenerator(HF_API_KEY)
    
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

if __name__ == "__main__":
    main()