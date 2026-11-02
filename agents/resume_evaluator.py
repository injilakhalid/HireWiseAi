import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas.job_schema import JobAnalysis
from schemas.resume_schema import ResumeEvaluation

load_dotenv()


def create_resume_evaluator():
    api_key = os.getenv("api_key")
    if not api_key:
        raise ValueError("API key not found. Check api_key in your project-root .env file.")

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
        google_api_key=api_key,
        temperature=0,
    )
    return llm.with_structured_output(ResumeEvaluation)


def evaluate_resume(resume_text: str, job_analysis: JobAnalysis) -> ResumeEvaluation:
    evaluator = create_resume_evaluator()
    prompt = f'''
You are an evidence-focused resume evaluator.

JOB ANALYSIS:
{job_analysis.model_dump_json(indent=2)}

CANDIDATE RESUME:
{resume_text}

Rules:
- Matching skills must be supported by evidence in the resume.
- "Missing skills" means required skills not evidenced in the resume, not proof
  the candidate does not possess them.
- Do not invent experience, qualifications, achievements, or certifications.
- Make the score an approximate alignment estimate, not a probability of hiring.
- Base the assessment on the stated job requirements and resume evidence.
- Give practical, truthful suggestions. Do not tell the candidate to claim skills
  they do not have.
'''
    return evaluator.invoke(prompt)
