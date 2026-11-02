
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas.job_schema import JobAnalysis
from schemas.resume_schema import ResumeEvaluation
from schemas.interview_schema import InterviewPlan


load_dotenv()


def create_interview_coach():
    """Create the LLM for interview preparation."""

    api_key = os.getenv("api_key")
    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

    if not api_key:
        raise ValueError("API key not found. Check your .env file.")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0,
        max_retries=0,
    )

    return llm.with_structured_output(InterviewPlan)


def generate_interview_plan(
    job_analysis: JobAnalysis,
    resume_evaluation: ResumeEvaluation,
) -> InterviewPlan:
    """Generate interview questions and a personalized study plan."""

    coach = create_interview_coach()

    prompt = f"""
You are an experienced technical interview coach.

Prepare a personalized interview preparation plan using
the job analysis and resume evaluation provided below.

Generate three sections:

1. TECHNICAL QUESTIONS
- Create relevant technical questions based on the job requirements.
- Cover the most important required skills and technologies.
- Include easy, medium, and hard questions.
- Explain the topic and why each question matters.

2. RESUME-BASED QUESTIONS
- Create questions based on the candidate's experience and projects.
- Ask about challenges, technical decisions, and results.
- Do not invent experience that is not present in the evaluation.

3. STUDY PLAN
- Create a prioritized, actionable study plan.
- Focus on important job requirements.
- Prioritize skills that are not evidenced in the resume.
- Make recommendations specific and practical.

For every interview question, provide:
- question
- topic
- difficulty
- reason

Return the result using the InterviewPlan schema.

JOB ANALYSIS:
{job_analysis.model_dump_json(indent=2)}

RESUME EVALUATION:
{resume_evaluation.model_dump_json(indent=2)}
"""

    result = coach.invoke(prompt)

    if isinstance(result, InterviewPlan):
        return result

    return InterviewPlan.model_validate(result)