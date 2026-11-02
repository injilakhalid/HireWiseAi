
import os
from unittest import result

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas.job_schema import JobAnalysis


# Load environment variables from the project-root .env file
load_dotenv()


def create_job_analyst():
    """Create the LLM with structured output for job analysis."""

    api_key = os.getenv("api_key")
    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

    if not api_key:
        raise ValueError(
            "API key not found. Check api_key in your project-root .env file."
        )

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0,
        max_retries=0,
    )

    return llm.with_structured_output(JobAnalysis)


def analyze_job(job_description: str) -> JobAnalysis:
    """Analyze a job description and return structured job requirements."""

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    analyst = create_job_analyst()

    prompt = f"""
You are an expert job-description analyst.

Analyze the job description and extract the following information:

1. Job title
2. Required technical and professional skills
3. Preferred or desirable skills
4. Main job responsibilities
5. Required education, experience, and certifications

Instructions:
- Use only information supported by the job description.
- Do not invent skills, responsibilities, or qualifications.
- Separate explicitly required skills from preferred skills.
- Keep each item concise and specific.
- Return the result according to the provided JobAnalysis schema.

JOB DESCRIPTION:
{job_description}
"""

    result = analyst.invoke(prompt)

       # Ensure the result is returned as a JobAnalysis object.
    if isinstance(result, JobAnalysis):
        return result

    return JobAnalysis.model_validate(result)