from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question")
    topic: str = Field(description="The topic being assessed")
    difficulty: str = Field(description="Beginner, Intermediate, or Advanced")
    reason: str = Field(description="Why this question is relevant")


class InterviewPlan(BaseModel):
    technical_questions: list[InterviewQuestion] = Field(description="Technical interview questions")
    resume_based_questions: list[InterviewQuestion] = Field(description="Questions based on resume evidence and gaps")
    study_plan: list[str] = Field(description="Prioritised preparation tasks")
