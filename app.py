import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="AI Study Buddy", layout="centered")

st.title("📚 AI Study Buddy")
st.write("Enter a topic to learn and test yourself!")

topic = st.text_input("Enter a topic")

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0

def parse_quiz(text):
    questions = []
    parts = text.split("Q")
    for part in parts[1:]:
        lines = part.strip().split("\n")
        q = lines[0]
        options = [l for l in lines if l.startswith(("A", "B", "C", "D"))]
        ans = ""
        for l in lines:
            if "Answer" in l:
                ans = l.split(":")[-1].strip()
        questions.append((q, options, ans))
    return questions

if st.button("Generate"):
    with st.spinner("Generating content..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Explain {topic}, give summary and 3 MCQ questions with options A-D and answers."}
                ]
            )
            output = response.choices[0].message.content
            st.session_state.quiz_data = parse_quiz(output)
            st.write(output)

        except:
            st.warning("API failed. Showing sample data.")
            sample = """Q1. What is Python?
A. Snake
B. Programming Language
C. Game
D. OS
Answer: B

Q2. Which is used for web apps?
A. HTML
B. Car
C. Tree
D. River
Answer: A

Q3. What is AI?
A. Artificial Intelligence
B. Animal
C. Ice Cream
D. Car
Answer: A"""
            st.session_state.quiz_data = parse_quiz(sample)
            st.write(sample)

# Quiz Section
if st.session_state.quiz_data:
    st.subheader("🧠 Quiz")
    user_answers = []

    for i, (q, options, ans) in enumerate(st.session_state.quiz_data):
        st.write(f"Q{i+1}. {q}")
        choice = st.radio("Select answer", options, key=i)
        user_answers.append((choice, ans))

    if st.button("Submit Answers"):
        score = 0
        for user, correct in user_answers:
            if user.startswith(correct):
                score += 1

        st.success(f"Your Score: {score}/{len(user_answers)}")
