# GenAI Learning Mentor: Python Programming

An interactive AI study assistant built with **Streamlit** and **Groq (Llama 3)** featuring RAG capabilities, personalized study plan generation, practice quizzes, and concept weakness diagnosis.

## Features
- **Ask Questions (RAG)**: Context-grounded Q&A over `sample_notes.txt`.
- **Generate Study Plan**: Structured 3-month CS roadmap generation.
- **Generate Quiz**: Self-assessment question generation.
- **Identify Weak Areas**: Automated debugging and concept tutoring.

## 📹 Demo Video
Watch the 3-minute application walkthrough:  
👉 **[Click Here to Watch the Demo Video](https://drive.google.com/file/d/1N1RSYfRGblkljKX9hb8KOzmTdMUM03ux/view?usp=sharing)**

---

## 📐 System Architecture

```mermaid
flowchart TD
    %% Nodes
    U([👤 CS Student / User])
    UI[🖥️ Streamlit Frontend Dashboard]
    
    subgraph LOCAL["📁 Local Application Context"]
        ENV[".env (GROQ_API_KEY)"]
        CACHE["@st.cache_data"]
        NOTES["sample_notes.txt"]
    end

    PE[🧠 Prompt Engineering Engine]

    subgraph GROQ["⚡ Groq Cloud Infrastructure"]
        API[Groq API Client]
        ROUTER{Failover Router}
        M1[🤖 llama-3.1-8b-instant]
        M2[🤖 llama-3.3-70b-versatile]
        M3[🤖 openai/gpt-oss-20b]
    end

    %% Data Flow
    U -->|1. Select Mode & Enter Query| UI
    ENV -.->|Load Secret| UI
    UI -->|2. Check Cache| CACHE
    CACHE -->|Read Notes| NOTES
    
    UI -->|3. User Input| PE
    NOTES -->|RAG Grounding Context| PE
    
    PE -->|4. Final Prompt| API
    API --> ROUTER
    ROUTER -->|Primary| M1
    ROUTER -->|Failover 1| M2
    ROUTER -->|Failover 2| M3
    
    M1 -->|5. st.write_stream Tokens| UI
    UI -->|6. Interactive Output| U

    %% Styling
    style LOCAL fill:#1e1e2e,stroke:#89b4fa,stroke-width:2px,color:#fff
    style GROQ fill:#11111b,stroke:#fab387,stroke-width:2px,color:#fff
    style UI fill:#313244,stroke:#a6e3a1,stroke-width:2px,color:#fff
    style PE fill:#45475a,stroke:#cba6f7,stroke-width:2px,color:#fff
