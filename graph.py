
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from schemas.job_schema import JobAnalysis
from schemas.resume_schema import ResumeEvaluation
from schemas.interview_schema import InterviewPlan

from agents.job_analyst import analyze_job
from agents.resume_evaluator import evaluate_resume
from agents.interview_coach import generate_interview_plan


class HireWiseState(TypedDict, total=False):
    job_description: str
    resume_text: str
    job_analysis: JobAnalysis
    resume_evaluation: ResumeEvaluation
    interview_plan: InterviewPlan


def job_analyst_node(state: HireWiseState) -> dict:
    job_description = state.get("job_description", "")

    return {
        "job_analysis": analyze_job(job_description)
    }


def resume_evaluator_node(state: HireWiseState) -> dict:
    resume_text = state.get("resume_text", "")
    job_analysis = state.get("job_analysis")

    if job_analysis is None:
        raise ValueError("Job analysis is missing from the workflow state.")

    return {
        "resume_evaluation": evaluate_resume(
            resume_text=resume_text,
            job_analysis=job_analysis,
        )
    }


def interview_coach_node(state: HireWiseState) -> dict:
    job_analysis = state.get("job_analysis")
    resume_evaluation = state.get("resume_evaluation")

    if job_analysis is None or resume_evaluation is None:
        raise ValueError(
            "Job analysis or resume evaluation is missing from the workflow state."
        )

    return {
        "interview_plan": generate_interview_plan(
            job_analysis=job_analysis,
            resume_evaluation=resume_evaluation,
        )
    }


def build_hirewise_graph():
    builder = StateGraph(HireWiseState)

    builder.add_node("job_analyst", job_analyst_node)
    builder.add_node("resume_evaluator", resume_evaluator_node)
    builder.add_node("interview_coach", interview_coach_node)

    builder.add_edge(START, "job_analyst")
    builder.add_edge("job_analyst", "resume_evaluator")
    builder.add_edge("resume_evaluator", "interview_coach")
    builder.add_edge("interview_coach", END)

    return builder.compile()
