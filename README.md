# HireWise AI

HireWise AI is a multi-agent application that helps candidates prepare for job applications and technical interviews.

## Features

- **Job Analyst:** Extracts job titles, required skills, preferred skills, responsibilities, and qualifications from job descriptions.
- **Resume Evaluator:** Compares resume content with job requirements, identifies matching and missing skills, and provides improvement suggestions.
- **Interview Coach:** Generates technical interview questions, resume-based questions, and a personalized study plan.
- **PDF Resume Upload:** Extracts text from uploaded resumes.
- **Interactive Interface:** Uses Streamlit to provide a simple user interface.

## Tech Stack

- Python
- LangGraph
- LangChain
- Google Gemini
- Pydantic
- Streamlit
- PyPDF

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/injilakhalid/HireWiseAi.git
cd HireWiseAi
```

### 2. Install dependencies

Install `uv` if it isn't already available, then run:

```bash
uv sync
```

If pytest is not included in your project dependencies, add it with:

```bash
uv add --dev pytest
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
api_key=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-flash-latest
```

Replace the placeholder with your actual Gemini API key. Never commit your `.env` file to GitHub.

### 4. Run the application

Run the command-line application:

```bash
uv run main.py
```

Or launch the Streamlit interface:

```bash
uv run streamlit run app.py
```

### 5. Run tests

```bash
uv run python -m pytest
```

## Architecture

The application uses a LangGraph workflow to coordinate three agents:

1. Job Analyst
2. Resume Evaluator
3. Interview Coach

Each agent performs a distinct task and passes structured results to the next stage.

## Future Improvements

- Improve resume parsing and evaluation.
- Add more detailed interview preparation plans.
- Expand automated testing.
- Deploy the Streamlit application.