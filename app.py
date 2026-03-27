import os
import pickle
from flask import Flask, render_template, request, session, redirect, url_for

# Import project modules
from utils.resume_parser import extract_resume_text
from utils.skill_extractor import extract_skills
from utils.section_checker import check_sections
from utils.resume_scorer import calculate_score

app = Flask(__name__)

app.secret_key = "resume_ai_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Load ML model
model = pickle.load(open("model/resume_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))


# ====================================
# Intelligent Suggestion Generator
# ====================================

def generate_suggestions(text, skills, missing_sections):

    suggestions = []

    text_lower = text.lower()
    word_count = len(text.split())

    if word_count < 200:
        suggestions.append(
            "Your resume is too short. Expand your projects and experience with more details."
        )

    if word_count > 900:
        suggestions.append(
            "Your resume is too long. Keep it within 1–2 pages for better ATS compatibility."
        )

    if "projects" in missing_sections:
        suggestions.append(
            "Add a Projects section to demonstrate your practical skills."
        )

    if "experience" in missing_sections:
        suggestions.append(
            "Include internship or work experience to strengthen your resume."
        )

    if "certifications" in missing_sections:
        suggestions.append(
            "Adding certifications can improve your chances of passing ATS filters."
        )

    if "education" in missing_sections:
        suggestions.append(
            "Make sure your Education section clearly shows degree and institution."
        )

    if len(skills) < 5:
        suggestions.append(
            "Add more technical skills relevant to your domain."
        )

    if "github" not in text_lower:
        suggestions.append(
            "Include your GitHub profile to showcase coding projects."
        )

    if "linkedin" not in text_lower:
        suggestions.append(
            "Add your LinkedIn profile link so recruiters can learn more about you."
        )

    if "summary" not in text_lower and "objective" not in text_lower:
        suggestions.append(
            "Add a professional summary at the beginning of your resume."
        )

    action_words = [
        "developed", "built", "implemented",
        "designed", "optimized", "created",
        "led", "managed", "improved"
    ]

    if not any(word in text_lower for word in action_words):
        suggestions.append(
            "Use strong action verbs like 'developed', 'implemented', or 'designed'."
        )

    suggestions = list(dict.fromkeys(suggestions))

    return suggestions[:7]


# ====================================
# Upload Route
# ====================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["resume"]

        if file.filename == "":
            return "No file selected"

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Extract text
        text = extract_resume_text(file_path)

        # Extract skills
        skills = extract_skills(text)

        # Check sections
        missing_sections = check_sections(text)

        # Calculate score
        score = calculate_score(skills, missing_sections, text)

        # ML Prediction
        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]

        # Resume Badge
        if score <= 40:
            ml_result = "❌ Bad Resume"
        elif score <= 60:
            ml_result = "⚠ Just Okay Resume"
        elif score <= 80:
            ml_result = "👍 Average Resume"
        else:
            ml_result = "⭐ Good Resume"

        # Generate suggestions
        suggestions = generate_suggestions(text, skills, missing_sections)

        # Store results in session
        session["result_data"] = {
            "score": score,
            "skills": skills,
            "suggestions": suggestions,
            "ml_result": ml_result
        }

        return render_template("analyzing.html")

    return render_template("index.html")


# ====================================
# Result Page Route
# ====================================

@app.route("/result")
def result():

    data = session.get("result_data")

    if not data:
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        score=data["score"],
        skills=data["skills"],
        suggestions=data["suggestions"],
        ml_result=data["ml_result"]
    )
@app.route("/ping")
def ping():
    return "alive"

# ====================================
# Run App
# ====================================

if __name__ == "__main__":

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)