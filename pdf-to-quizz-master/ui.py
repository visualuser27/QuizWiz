import streamlit as st
import os
import json
import asyncio
import urllib.parse
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from generate_pdf import generate_pdf_quiz
import os

# Ensure 'data' directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Handle file upload
uploaded_file = st.file_uploader("📄 Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    # Replace spaces with underscores or use URL encoding
    safe_file_name = urllib.parse.quote(file_name.replace(" ", "_"))

    file_path = f"data/{safe_file_name}"

    # Save the uploaded file to the data directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.success(f"File '{file_name}' uploaded successfully and saved as '{safe_file_name}'.")

# Initialize session state
if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = None
if 'questions' not in st.session_state:
    st.session_state['questions'] = []

# Ensure 'data' directory exists
if not os.path.exists("data"):
    os.makedirs("data")

st.title("PDF to Quiz 😊")

# Function to display questions
def build_question(count, json_question):
    if json_question.get("question") is not None:
        st.write(f"**Question {count + 1}:** {json_question.get('question', '')}")
        choices = ['A', 'B', 'C', 'D']
        selected_answer = st.selectbox("Select your answer:", choices, key=f"select_{count}")
        for choice in choices:
            choice_str = json_question.get(choice, "None")
            st.write(f"{choice}: {choice_str}")
        
        if st.button("Submit", key=f"button_{count}"):
            correct_answer = json_question.get("reponse")
            if selected_answer == correct_answer:
                st.success(f"Correct! The answer is {correct_answer}.")
            else:
                st.error(f"Wrong! The correct answer is {correct_answer}.")
        count += 1
    return count

# File upload
uploaded_file = st.file_uploader("📄 Upload your PDF file", type=["pdf"])

# Text input for quiz generation
txt = st.text_area("Enter text to generate a quiz:")

if st.button("Generate Quiz", key="button_generate_text"):
    if txt.strip():
        with st.spinner("Generating quiz..."):
            st.session_state['questions'] = asyncio.run(txt_to_quizz(txt))
            st.success("Quiz generated successfully!")

if uploaded_file:
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if old_file_name != uploaded_file.name:
        with st.spinner("Generating quiz from PDF..."):
            # Ensure safe file name
            file_name = uploaded_file.name
            safe_file_name = urllib.parse.quote(file_name.replace(" ", "_"))
            file_path = f"data/{safe_file_name}"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['questions'] = asyncio.run(pdf_to_quizz(file_path))
            st.success("Quiz generated successfully!")

if 'questions' in st.session_state and st.session_state['questions']:
    count = 0
    for json_question in st.session_state['questions']:
        count = build_question(count, json_question)

    # Generate PDF Quiz
    if st.button("Generate PDF Quiz", key="button_generate_pdf"):
        with st.spinner("Generating PDF quiz..."):
            file_name = uploaded_file.name if uploaded_file else "text_input"
            if file_name.endswith(".pdf"):
                file_name = file_name[:-4]

            json_file_path = f"data/quiz-{file_name}.json"
            with open(json_file_path, "w", encoding="latin-1", errors="ignore") as f:
                json.dump(st.session_state['questions'], f)

            generate_pdf_quiz(json_file_path, st.session_state['questions'])
            st.success("PDF Quiz generated successfully!")
