import streamlit as st

from graph import build_hirewise_graph
from utils.pdf_reader import extract_text_from_pdf

st.set_page_config(page_title="HireWise AI", page_icon="🧭", layout="wide")
st.title("🧭 HireWise AI")
st.caption("Analyse a job, compare your resume, and prepare for interviews.")

with st.form("hirewise_form"):
    job_description = st.text_area(
        "Job description",
        height=260,
        placeholder="Paste the complete job description here...",
    )
    resume_file = st.file_uploader("Upload your resume (text-based PDF)", type=["pdf"])
    submitted = st.form_submit_button("Analyse my application")

if submitted:
    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()
    if resume_file is None:
        st.error("Please upload a resume PDF.")
        st.stop()

    try:
        with st.spinner("Extracting resume text..."):
            resume_text = extract_text_from_pdf(resume_file.getvalue())

        with st.spinner("Running the three-agent workflow. This uses Gemini API quota..."):
            workflow = build_hirewise_graph()
            result = workflow.invoke({
                "job_description": job_description,
                "resume_text": resume_text,
            })

        job = result["job_analysis"]
        evaluation = result["resume_evaluation"]
        plan = result["interview_plan"]

        st.success("Analysis complete!")
        st.header("1. Job analysis")
        st.subheader(job.job_title)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Required skills**")
            st.write(job.required_skills or ["None explicitly identified"])
            st.markdown("**Preferred skills**")
            st.write(job.preferred_skills or ["None explicitly identified"])
        with col2:
            st.markdown("**Responsibilities**")
            st.write(job.responsibilities or ["None identified"])
            st.markdown("**Qualifications**")
            st.write(job.qualifications or ["None identified"])

        st.header("2. Resume evaluation")
        st.metric("Estimated resume-to-role alignment", f"{evaluation.match_score}/100")
        st.caption("This is an AI-generated estimate, not a probability of getting hired.")
        st.write(evaluation.summary)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Skills supported by resume evidence**")
            st.write(evaluation.matching_skills or ["None identified"])
            st.markdown("**Required skills not evidenced**")
            st.write(evaluation.missing_skills or ["None identified"])
        with col2:
            st.markdown("**Relevant experience**")
            st.write(evaluation.relevant_experience or ["None identified"])
            st.markdown("**Improvement suggestions**")
            st.write(evaluation.improvement_suggestions or ["None identified"])

        st.header("3. Interview preparation")
        st.subheader("Technical questions")
        for i, q in enumerate(plan.technical_questions, 1):
            with st.expander(f"{i}. {q.question}"):
                st.write(f"**Topic:** {q.topic}")
                st.write(f"**Difficulty:** {q.difficulty}")
                st.write(f"**Why it matters:** {q.reason}")

        st.subheader("Resume-based questions")
        for i, q in enumerate(plan.resume_based_questions, 1):
            with st.expander(f"{i}. {q.question}"):
                st.write(f"**Topic:** {q.topic}")
                st.write(f"**Difficulty:** {q.difficulty}")
                st.write(f"**Why it matters:** {q.reason}")

        st.subheader("Prioritised study plan")
        for i, task in enumerate(plan.study_plan, 1):
            st.write(f"{i}. {task}")

    except Exception as exc:
        st.error("The workflow could not complete.")
        st.exception(exc)
        st.info(
            "If the error is a Gemini quota (429) or availability (503) error, "
            "the code may be fine. Check your Google AI Studio quota and retry later."
        )
