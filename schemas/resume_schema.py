from pydantic import BaseModel, Field


class ResumeEvaluation(BaseModel):
    match_score: int = Field(ge=0, le=100, description="Estimated alignment score from 0 to 100")
    matching_skills: list[str] = Field(description="Job skills supported by resume evidence")
    missing_skills: list[str] = Field(description="Required skills not evidenced in the resume")
    relevant_experience: list[str] = Field(description="Relevant experience supported by the resume")
    improvement_suggestions: list[str] = Field(description="Specific, truthful resume improvements")
    summary: str = Field(description="Concise assessment of the candidate's alignment")
