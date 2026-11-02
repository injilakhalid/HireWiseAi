from graph import build_hirewise_graph

SAMPLE_JOB_DESCRIPTION = '''
We are looking for a Data Engineer.

Responsibilities:
- Design and maintain ETL pipelines.
- Develop data processing applications using Python.
- Write complex SQL queries and stored procedures.
- Build data warehouse solutions using Snowflake.
- Work with Databricks and cloud platforms.

Requirements:
- Strong Python and SQL skills.
- Experience with ETL and ELT pipelines.
- Knowledge of Snowflake.
- Familiarity with Databricks and cloud technologies.
'''

SAMPLE_RESUME = '''
SUMMARY:
Data professional with experience in Python, SQL, and data analytics.

SKILLS:
Python, SQL, Power BI, pandas.

PROJECTS:
Developed a Power BI dashboard for monitoring operational performance.
Used Python to analyse data and identify trends.
Wrote SQL queries to retrieve and transform data.
'''

if __name__ == "__main__":
    print("Running HireWise AI workflow. This makes Gemini API calls.")
    workflow = build_hirewise_graph()
    result = workflow.invoke({
        "job_description": SAMPLE_JOB_DESCRIPTION,
        "resume_text": SAMPLE_RESUME,
    })

    job = result["job_analysis"]
    evaluation = result["resume_evaluation"]
    plan = result["interview_plan"]

    print(f"\nJOB TITLE: {job.job_title}")
    print(f"\nESTIMATED MATCH: {evaluation.match_score}/100")
    print(f"\nSUMMARY: {evaluation.summary}")

    print("\nSKILLS NOT EVIDENCED IN RESUME")
    for skill in evaluation.missing_skills:
        print(f"- {skill}")

    print("\nTECHNICAL INTERVIEW QUESTIONS")
    for item in plan.technical_questions:
        print(f"- [{item.difficulty}] {item.question} ({item.topic})")

    print("\nRESUME-BASED QUESTIONS")
    for item in plan.resume_based_questions:
        print(f"- {item.question}")

    print("\nSTUDY PLAN")
    for index, item in enumerate(plan.study_plan, start=1):
        print(f"{index}. {item}")
