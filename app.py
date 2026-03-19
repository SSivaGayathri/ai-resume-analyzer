from PyPDF2 import PdfReader
from flask import Flask, render_template, request
import numpy as np
import re

app = Flask(__name__, template_folder='templates', static_folder='static')

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# 📊 Analyze Route
@app.route('/analyze', methods=['POST'])
def analyze():
    resume_text = ""

    # 📂 Get uploaded file
    file = request.files.get('resume')
    print("FILE:", file)

    # 📄 Extract PDF text
    if file and file.filename!="":
        reader = PdfReader(file)

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    # 📝 Fallback (if no file uploaded)
    if not resume_text.strip():
        return "❌ No text extracted from PDF. Try another file."

    # ❗ Debug (check if text is coming)
    print("RAW TEXT:", resume_text[:300])

    # 🔤 Clean text (VERY IMPORTANT 🔥)
    resume_text = resume_text.lower()
    resume_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', resume_text)

    print("CLEAN TEXT:", resume_text[:300])

    # 🎯 Get selected role
    role = request.form.get('role')

    # 🧠 Role-based skills
    if role == "frontend":
        skills = ["html", "css", "javascript", "react"]

    elif role == "data":
        skills = ["python", "sql", "pandas", "numpy", "machine learning"]

    elif role == "python":
        skills = ["python", "flask", "django", "sql"]

    else:
        skills = ["python", "html", "css", "sql"]

    matched = []
    missing = []

    # 🔍 Improved Skill Matching
    for skill in skills:
        if skill in resume_text:
            matched.append(skill.capitalize())
        else:
            # 🔥 handle variations
            if skill == "react" and "react js" in resume_text:
                matched.append("React")
            elif skill == "python" and ("python3" in resume_text or "python 3" in resume_text):
                matched.append("Python")
            elif skill == "machine learning" and ("ml" in resume_text):
                matched.append("Machine Learning")
            else:
                missing.append(skill.capitalize())

    # 📊 Score
    if len(skills) > 0:
        score = (len(matched) / len(skills)) * 100
    else:
        score = 0

    score = np.round(score, 2)

    # 🤖 Suggestions
    suggestions = []
    for skill in missing:
        suggestions.append(f"Consider learning {skill} to improve your profile.")

    # 🎯 Render result
    return render_template(
        'result.html',   # keep this same as your file name
        matched=matched,
        missing=missing,
        score=score,
        suggestions=suggestions
    )


# ▶️ Run App
import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)









    
