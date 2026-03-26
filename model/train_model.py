from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load ML model and vectorizer
model = pickle.load(open("model/resume_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))


# Skills list for ATS scoring
skills_list = [
    "python","java","c++","sql","machine learning","deep learning",
    "data analysis","pandas","numpy","flask","django","html","css",
    "javascript","react","node","docker","kubernetes","aws","git"
]


# -------------------------------
# ATS SCORE FUNCTION
# -------------------------------
def calculate_ats_score(resume_text):

    text = resume_text.lower()
    score = 0

    # Skill match
    for skill in skills_list:
        if skill in text:
            score += 4

    # Section checks
    if "project" in text:
        score += 10

    if "experience" in text:
        score += 10

    if "education" in text:
        score += 5

    if "certification" in text:
        score += 5

    if "github" in text:
        score += 5

    if "linkedin" in text:
        score += 5

    return min(score, 100)


# -------------------------------
# BADGE SYSTEM
# -------------------------------
def get_badge(score):

    if score < 40:
        return "Bad Resume ❌"
    elif score < 60:
        return "Just OK ⚠"
    elif score < 80:
        return "Average 👍"
    else:
        return "Good Resume 🏆"


# -------------------------------
# AI SUGGESTION SYSTEM
# -------------------------------
def generate_suggestions(resume_text, ats_score):

    suggestions = []
    text = resume_text.lower()

    # Section suggestions
    if "project" not in text:
        suggestions.append("Add a Projects section to showcase your practical work.")

    if "skill" not in text:
        suggestions.append("Include a Skills section listing technologies you know.")

    if "experience" not in text:
        suggestions.append("Mention internships or work experience.")

    if "education" not in text:
        suggestions.append("Add your educational qualifications.")

    if "github" not in text:
        suggestions.append("Add your GitHub profile to show coding projects.")

    if "linkedin" not in text:
        suggestions.append("Include your LinkedIn profile for professional visibility.")

    # Achievement detection
    if not re.search(r"\d+%", text):
        suggestions.append("Add measurable achievements (example: improved system performance by 30%).")

    # Score-based improvements
    if ats_score < 50:
        suggestions.append("Your resume needs more technical keywords relevant to the job.")
        suggestions.append("Add projects and certifications to improve your ATS score.")

    elif ats_score < 70:
        suggestions.append("Your resume is decent but could be improved with more project details.")
        suggestions.append("Highlight specific tools and technologies you used.")

    elif ats_score < 85:
        suggestions.append("Good resume. Add leadership roles or team collaborations.")

    else:
        suggestions.append("Excellent resume! Consider tailoring it for specific job roles.")

    return suggestions


# -------------------------------
# MAIN ROUTE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        resume_text = request.form["resume_text"]

        # ATS Score
        ats_score = calculate_ats_score(resume_text)

        # Badge
        badge = get_badge(ats_score)

        # ML Prediction
        resume_vector = vectorizer.transform([resume_text])
        prediction = model.predict(resume_vector)

        ml_result = "Selected" if prediction[0] == 1 else "Not Selected"

        # AI Suggestions
        suggestions = generate_suggestions(resume_text, ats_score)

        return render_template(
            "result.html",
            ats_score=ats_score,
            badge=badge,
            ml_result=ml_result,
            suggestions=suggestions
        )

    return render_template("index.html")


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)