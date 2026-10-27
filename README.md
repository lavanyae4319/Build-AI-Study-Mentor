# AI Study Mentor 🎓

## Overview
AI Study Mentor is an interactive learning application that helps students understand technical topics, create study plans, and practice through AI-generated quizzes.

## Features
- **AI Study Assistant:** Explains topics with beginner-friendly examples.
- **Study Planner:** Generates day-by-day study plans.
- **AI Quiz Generator:** Creates quizzes for different subjects, question counts, and difficulty levels.
- **Quiz Results:** Calculates scores and explains correct answers.
- **Progress Tracker:** Tracks activity and the best quiz score during the current session.

## Technology Stack
- Python
- Streamlit
- Groq API
- Python dotenv

## Installation

1. Install Python.
2. Clone or download this repository.
3. Open the project folder in a terminal.
4. Create and activate a virtual environment.
5. Install dependencies:

   `python -m pip install -r requirements.txt`

6. Create a `.env` file in the root folder:

   `GROQ_API_KEY=your_groq_api_key`

   `GROQ_MODEL=openai/gpt-oss-120b`

   Replace the placeholder with your own API key. Never publish it.

7. Run the application:

   `python -m streamlit run frontend/app.py`

8. Open the local URL displayed in the terminal.

## How It Works
The user selects a topic or quiz configuration. The application sends a request to the Groq API, displays the generated response, and presents quiz results with explanations.

## Limitations
- An internet connection and a valid API key are required for AI features.
- AI-generated answers may occasionally be inaccurate and should be reviewed.
- Progress is stored in the current Streamlit session and is not a permanent user history.

## Future Improvements
- Persistent user accounts and progress
- Additional question formats
- Quiz history and performance analytics
