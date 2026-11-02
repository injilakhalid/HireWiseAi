from pydantic import BaseModel, Field


class JobAnalysis(BaseModel):
    job_title: str = Field(description="Job title identified in the job description")
    required_skills: list[str] = Field(description="Skills explicitly required")
    preferred_skills: list[str] = Field(description="Skills explicitly marked preferred or desirable")
    responsibilities: list[str] = Field(description="Main responsibilities")
    qualifications: list[str] = Field(description="Education, experience, or certifications required")
