import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="GenAI Learning Mentor", page_icon="🤖", layout="wide")
st.title("🤖 GenAI Learning Mentor: Python Programming")
st.caption("Your interactive AI study assistant powered by Groq")

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found in .env file. Please add it to continue.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Active Groq models in priority order for failover
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b"
]

# 2. Sidebar Navigation
st.sidebar.header("🎯 Mentor Options")
mode = st.sidebar.radio(
    "Choose Action:",
    ["Ask Questions (RAG)", "Generate Study Plan", "Generate Quiz", "Identify Weak Areas"]
)

# Cache notes to avoid repeated disk reads
@st.cache_data
def load_notes():
    if os.path.exists("sample_notes.txt"):
        with open("sample_notes.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No course notes found."

notes_content = load_notes()

# Fast streaming function with model fallback
def stream_groq_response(prompt):
    for model_name in AVAILABLE_MODELS:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                stream=True
            )
            for chunk in completion:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            return
        except Exception:
            continue
            
    st.error("Groq API Error: Unable to reach active models. Check API status or key permissions.")

# 3. Feature Modes
if mode == "Ask Questions (RAG)":
    st.subheader("📚 Ask Anything From Your Python Notes")
    user_query = st.text_input("Enter your question:", placeholder="e.g., What is the difference between list and tuple?")
    
    if user_query:
        prompt = f"""
        You are an expert Python tutor. Use the course notes below to answer directly in clear markdown with code examples.
        
        Course Notes:
        {notes_content}
        
        Question: {user_query}
        """
        st.markdown("### Answer")
        st.write_stream(stream_groq_response(prompt))

elif mode == "Generate Study Plan":
    st.subheader("🗓️ Personal Study Roadmap")
    goal = st.text_input("Goal:", value="Master Python Data Structures in 3 months")
    
    if st.button("Build Plan"):
        prompt = f"""
        You are an expert Computer Science mentor. Generate a detailed, structured 3-month study plan for a student with the goal: '{goal}'.
        
        Format the output clearly using Markdown headers and bullet points:
        - **Month 1**: Core Basics & Linear Data Structures (Lists, Tuples, Stacks, Queues)
        - **Month 2**: Non-Linear Data Structures (Trees, Graphs, Hash Maps/Dicts)
        - **Month 3**: Algorithms & Practical Projects (Sorting, Searching, LeetCode practice)
        
        Include weekly focus topics and recommended practice tasks for each month.
        """
        st.markdown("### Study Plan")
        st.write_stream(stream_groq_response(prompt))

elif mode == "Generate Quiz":
    st.subheader("📝 Practice Quiz")
    if st.button("Generate Quiz"):
        prompt = """
        Generate 3 multiple-choice practice questions on Python data structures. 
        Provide choices (A, B, C, D) and include the correct answers at the bottom under a spoiler answer section.
        """
        st.markdown("### Quiz")
        st.write_stream(stream_groq_response(prompt))

elif mode == "Identify Weak Areas":
    st.subheader("⚠️ Weak Area Diagnosis")
    problem = st.text_area("What concept or code is giving you trouble?", placeholder="e.g., I don't understand recursion.")
    if problem:
        prompt = f"""
        You are a CS mentor. Explain this concept simply and clearly with a minimal Python code example: {problem}
        """
        st.markdown("### Explanation")
        st.write_stream(stream_groq_response(prompt))