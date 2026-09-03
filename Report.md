# Project Report: GenAI Learning Mentor
**Course / Project**: Project 6 — GenAI Learning Mentor  
**Developer**: Vikhyat Gupta  
**Tech Stack**: Python, Streamlit, Groq Cloud API, Meta Llama 3 Models, RAG Architecture  

---

## 1. Executive Summary

In computer science education, students frequently face challenges synthesizing long-form course materials, diagnosing conceptual misunderstandings, and building structured, long-term study roadmaps. While generic LLM interfaces provide broad answers, they often lack domain-specific context grounding, which can lead to hallucinations or overly generic code explanations.

The **GenAI Learning Mentor** is an interactive, lightweight study assistant built specifically for Computer Science students studying Python programming and data structures. The application provides four core functional modules within a unified Streamlit dashboard:
1. **Knowledge-Grounded Q&A (RAG)** over local course notes (`sample_notes.txt`).
2. **Personalized 3-Month Study Roadmap Generation**.
3. **Practice Quiz Generation** with hidden answer keys.
4. **Weak Area Concept Diagnosis** with minimal, clear code examples.

---

## 2. System Architecture & Component Design

```text
+-----------------------------------------------------------------------+
|                           FRONTEND LAYER                              |
|   Streamlit Web Interface (app.py)                                    |
|   - Multi-Tab Sidebar Navigation (RAG, Study Plan, Quiz, Diagnostic)  |
|   - Real-Time Token Rendering via st.write_stream                     |
+-----------------------------------++----------------------------------+
                                    ||
                                    \/
+-----------------------------------------------------------------------+
|                           LOGIC & RAG LAYER                           |
|   - Environment Security (python-dotenv for GROQ_API_KEY)             |
|   - Local Knowledge Base (@st.cache_data for sample_notes.txt)        |
|   - Task-Specific Prompt Engineering Router                           |
+-----------------------------------++----------------------------------+
                                    ||
                                    \/
+-----------------------------------------------------------------------+
|                       GROQ INFERENCE CLOUD API                        |
|   - REST/HTTP Transport Protocol                                      |
|   - Sequential Automated Model Failover Router:                       |
|       1. llama-3.1-8b-instant (Primary)                               |
|       2. llama-3.3-70b-versatile (Secondary)                           |
|       3. openai/gpt-oss-20b (Tertiary)                                |
+-----------------------------------------------------------------------+

```

### Component Breakdown

* **Frontend (`app.py`)**: Built with Streamlit, providing a reactive single-page interface for switching between learning modes.
* **Knowledge Base (`sample_notes.txt`)**: Acts as local domain-specific memory, grounding model responses during Q&A interactions.
* **Inference Engine (Groq API)**: Leverages Groq's LPU (Language Processing Unit) infrastructure to deliver high-throughput, streaming responses.

---

## 3. Prompt Engineering Strategy

To ensure deterministic, high-quality, and structured outputs across different study modes, custom system prompts were designed:

### A. RAG Q&A Mode

```text
System: You are an expert Python tutor. 
Instruction: Use the course notes below to answer directly in clear markdown with code examples. 
Grounding Context: {notes_content}
User Query: {user_query}

```

* **Objective**: Forces strict grounding on course notes, suppressing model hallucinations and irrelevant external details.

### B. Study Plan Generation Mode

```text
System: You are an expert Computer Science mentor.
Instruction: Generate a detailed, structured 3-month study plan for a student with the goal: '{goal}'.
Format Requirements:
- Month 1: Core Basics & Linear Data Structures (Lists, Tuples, Stacks, Queues)
- Month 2: Non-Linear Data Structures (Trees, Graphs, Hash Maps/Dicts)
- Month 3: Algorithms & Practical Projects (Sorting, Searching, LeetCode practice)
Include weekly focus topics and recommended practice tasks for each month.

```

* **Objective**: Enforces explicit structural Markdown formatting to ensure comprehensive output generation.

---

## 4. Technical Challenges & Solutions Log

| Engineering Challenge | Root Cause | Implemented Solution |
| --- | --- | --- |
| **API Endpoint Deprecations (`404 NOT_FOUND`)** | Deprecation of legacy model strings across cloud API providers. | Migrated architecture to Groq API using active Llama 3 endpoints. |
| **High Demand Service Spikes (`503 UNAVAILABLE`)** | Sudden server capacity limits on free tier endpoints. | Implemented a sequential `AVAILABLE_MODELS` list with automatic try/except fallback routing. |
| **Network Stalls / Infinite Loading** | macOS gRPC HTTP/2 handshake freezes in Anaconda Python environments. | Switched to standard HTTP REST transport calls and stream yields via `st.write_stream`. |
| **Incomplete Study Plan Output** | Restrictive default `max_output_tokens` parameters truncating long text. | Removed token length caps and added explicit structural formatting rules inside system prompts. |

---

## 5. Local Setup & Execution Guide

### Prerequisites

* Python 3.10+
* Free Groq API Key ([console.groq.com](https://console.groq.com/))

### Installation Steps

1. **Clone the repository**:
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd LLM_Project

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Set up environment variables**:
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_actual_groq_api_key_here

```


4. **Run the Application**:
```bash
streamlit run app.py

```



---

## 6. Conclusion & Future Enhancements

The **GenAI Learning Mentor** successfully delivers a responsive, context-grounded, and multi-featured assistant for CS students.

### Future Roadmap

* **Vector Database Integration**: Upgrade flat-file reading to FAISS vector embeddings for multi-document textbook retrieval.
* **Persistent Session Memory**: Implement Streamlit session state (`st.session_state`) to maintain long multi-turn conversation context.

```

```
