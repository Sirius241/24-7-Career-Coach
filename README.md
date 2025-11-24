# 24-7-Career-Coach 💻
AI agent as a Career Coach

## Overview
An AI-powered platform that mimics high-pressure interview environments to help candidates prepare for technical, behavioral, and situational rounds. Built with Google Gemini, the system adapts dynamically to user responses, listens to voice input, analyzes answers in real time, and generates a professional PDF performance report for actionable feedback.

## Architecture
- **Frontend Layer (Streamlit)**  
  - Provides a lightweight, interactive UI for candidates.  
  - Handles voice input via `streamlit-mic-recorder`.  
  - Renders adaptive interview questions and feedback in real time.  

- **AI Layer (Google Gemini)**  
  - Core intelligence for generating technical, behavioral, and situational questions.  
  - Performs semantic analysis of candidate responses.  
  - Adapts difficulty and follow-ups based on performance.  

- **Audio Processing**  
  - Captures candidate voice input.  
  - Transcribes speech to text for Gemini analysis.  
  - Ensures natural interview flow without manual typing.  

- **Evaluation & Feedback Engine**  
  - Applies rubric-based scoring (clarity, correctness, communication).  
  - Tracks response history to identify strengths and weaknesses.  
  - Generates structured feedback for each round.  

- **Report Generation (FPDF)**  
  - Converts session data into a professional PDF report.  
  - Includes scores, improvement suggestions, and summary charts. 

## Tech Stack
- Frontend: Streamlit (Python)
- AI Model: Google Gemini 
- Audio: streamlit-mic-recorder
- Report Generation: FPDF

## Workflow
- Candidate initiates a mock interview session
- AI agent conducts adaptive rounds
- Voice input is captured and transcribed
- Responses are analyzed in real time
- PDF performance report is generated

## Installation

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Steps
1. **Clone the repository**
   
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   #Windows
   venv\Scripts\activate
   #macOS / Linux
   source venv/bin/activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Add environment variables**
   Create a .env file in the project root:
   ```bash
   GEMINI_API_KEY=your_api_key_here

5. **Run the app**
   ```bash
   streamlit run app.py
  

## 🎯 Use Cases
- Students preparing for campus placements
- Professionals practicing for FAANG/Big Tech interviews
- Career coaches offering structured mock interviews
- Self-learners seeking feedback loops
