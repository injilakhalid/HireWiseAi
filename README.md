# HireWise AI — starter project

A beginner-friendly multi-agent job application assistant using Gemini, LangChain, LangGraph, Pydantic, pypdf, and Streamlit.

## Important
- This is a starter/reference project. Copy the files into your existing project carefully; do not overwrite your `.env`.
- Your existing environment variable name is `api_key`, so the code reads `api_key` from `.env`.
- Running the app calls Gemini and uses API quota. Tests do not call Gemini.
- Never commit `.env` or share your API key.

## Expected structure
```text
analysis_project/
├── .env
├── main.py
├── app.py
├── graph.py
├── agents/
│   ├── __init__.py
│   ├── job_analyst.py
│   ├── resume_evaluator.py
│   └── interview_coach.py
├── schemas/
│   ├── __init__.py
│   ├── job_schema.py
│   ├── resume_schema.py
│   └── interview_schema.py
├── utils/
│   ├── __init__.py
│   └── pdf_reader.py
└── tests/
    └── test_pdf_reader.py
```

## Install dependencies (from your project folder)
```powershell
uv add langgraph langchain-google-genai langchain-core pydantic python-dotenv streamlit pypdf
```

## Configure `.env`
Keep your existing `.env` file. It should contain:
```text
api_key=YOUR_REAL_GEMINI_API_KEY
```

## Run without UI
```powershell
uv run main.py
```

## Run the web app
```powershell
uv run streamlit run app.py
```

## Run offline tests (no Gemini API calls)
```powershell
uv run python -m pytest
```
If pytest is not installed:
```powershell
uv add --dev pytest
uv run python -m pytest
```

## Notes
- `graph.py` uses a simple sequential LangGraph: Job Analyst → Resume Evaluator → Interview Coach.
- LLM-generated match scores are estimates, not calibrated probabilities.
- Missing resume evidence means "not shown in this resume", not necessarily that the candidate lacks the skill.
- For API failures (429, 503, network errors), check Google AI Studio and the official Gemini API quota/status documentation.
