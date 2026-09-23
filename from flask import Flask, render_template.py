from flask import Flask, render_template, request

app = Flask(__name__)

# Skills our system can identify
skills_list = [
    "python", "java", "sql", "html", "css",
    "javascript", "react", "node", "flask",
    "machine learning", "data analysis",
    "git", "docker", "aws"
]

# Sample jobs
jobs = [
    {
        "title": "Python Developer",
        "company": "TCS",
        "skills": ["python", "sql", "flask"],
        "salary": "5-8 LPA"
    },
    {
        "title": "Data Analyst",
        "company": "Accenture",
        "skills": ["python", "sql", "data analysis"],
        "salary": "4-7 LPA"
    },
    {
        "title": "Frontend Developer",
        "company": "Freshworks",
        "skills": ["html", "css", "javascript", "react"],
        "salary": "5-9 LPA"
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Infosys",
        "skills": ["python", "machine learning", "sql", "aws"],
        "salary": "7-12 LPA"
    }
]


def find_skills(resume):
    found = []

    for skill in skills_list:
        if skill in resume.lower():
            found.append(skill)

    return found


def calculate_ats(found_skills):
    score = 40 + len(found_skills) * 4

    return min(score, 100)


def find_jobs(found_skills):

    results = []

    for job in jobs:

        matched = 0

        for skill in job["skills"]:

            if skill in found_skills:
                matched += 1

        match = int(
            matched / len(job["skills"]) * 100
        )

        if match > 0:

            results.append({
                "title": job["title"],
                "company": job["company"],
                "salary": job["salary"],
                "match": match
            })

    return sorted(
        results,
        key=lambda x: x["match"],
        reverse=True
    )


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        resume = request.form["resume"]

        skills = find_skills(resume)

        ats = calculate_ats(skills)

        recommended_jobs = find_jobs(skills)

        result = {
            "skills": skills,
            "ats": ats,
            "jobs": recommended_jobs
        }

    return render_template(
        "index.html",
        result=result
    )


app.run(debug=True)