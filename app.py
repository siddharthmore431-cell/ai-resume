from flask import Flask, render_template, request
import os
from pdfminer.high_level import extract_text
import docx

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create resumes folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    score = None

    if request.method == "POST":
        resume = request.files["resume"]
        job_description = request.form["job"]

        if resume:
            resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
            resume.save(resume_path)

            resume_text = read_resume(resume_path)
            score = calculate_match(resume_text, job_description)

    return render_template("index.html", score=score)

def read_resume(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        text = extract_text(file_path)

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + " "

    else:
        with open(file_path, "r", errors="ignore") as f:
            text = f.read()

    return text

def calculate_match(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    if len(job_words) == 0:
        return 0

    matched = resume_words.intersection(job_words)
    score = (len(matched) / len(job_words)) * 100

    return round(score, 2)

if __name__ == "__main__":
    app.run(debug=True)