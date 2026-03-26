def extract_skills(text):

    skills_db = [
        "python",
        "java",
        "c++",
        "sql",
        "machine learning",
        "data analysis",
        "pandas",
        "numpy",
        "flask",
        "html",
        "css",
        "javascript",
        "react",
        "django"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills