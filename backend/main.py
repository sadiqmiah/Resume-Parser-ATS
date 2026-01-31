from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from spacy.cli import download
import re
import spacy
import os
import spacy.cli
from pathlib import Path
import pdfplumber

# Load spaCy NER model
model_name = "en_core_web_sm"
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

app = FastAPI(title="Resume Parser (ATS) API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Resume Parser ATS is running"}

UPLOAD_DIR = Path("resumes")
UPLOAD_DIR.mkdir(exist_ok=True)

def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Skills
SKILLS = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "Git",
    "Docker", "AWS", "React", "Node.js", "Express.js", "PostgreSQL", "MongoDB",
    "Bootstrap", "jQuery", "Adobe Photoshop", "Figma", "Canva"
]

def parse_entities(text):
    doc = nlp(text)
    result = {
        "Name": [],
        "Email": [],
        "Phone": [],
        "LinkedIn": [],
        "Skills": [],
        "Experience": [],
        "Education": [],
        "Certifications": []
    }

    # Name
    lines = text.split("\n")
    for line in lines:
        line_clean = line.strip()
        if len(line_clean.split()) <= 4 and all(word[0].isupper() for word in line_clean.split()):
            result["Name"] = [line_clean]
            break

    # Email and phone
    result["Email"] = list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))
    phones = re.findall(r"\+?\d[\d\s().-]{7,}\d", text)
    clean_phones = []
    for p in phones:
        if '(' in p:
            p = p[p.find('('):]  # remove stray numbers before '('
        p = re.sub(r"\s+", "", p)
        clean_phones.append(p)
    result["Phone"] = clean_phones

    # LinkedIn
    linkedin = re.findall(r"https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", text)
    result["LinkedIn"] = linkedin

    # Skills
    SKILLS = [
        "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "Git",
        "Docker", "AWS", "React", "Node.js", "Express.js", "PostgreSQL", "MongoDB",
        "Bootstrap", "jQuery", "Adobe Photoshop", "Figma", "Canva"
    ]
    result["Skills"] = sorted(list({skill for skill in SKILLS if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)}))

    # Look for ORG entities but filter only your job/company
    experience_lines = []
    for line in text.splitlines():
        if "Best Copy" in line:
            experience_lines.append("Best Copy and Shipping New York City, NY")
            break
    result["Experience"] = experience_lines

    # Projects
    project_keywords = ["Nested Loops", "Student Grades Management System", "Fibonacci"]
    projects = []
    for line in text.splitlines():
        if any(keyword in line for keyword in project_keywords):
            projects.append(line.strip())
    result["Projects"] = projects

    # Education
    edu_matches = re.findall(
        r"(Queens College.*?City University of New York|City University of New York.*?Queens College)",
        text,
        flags=re.DOTALL
    )
    result["Education"] = [e.replace("\n", " ").strip() for e in edu_matches]

    # Certifications (look for keywords like "Certificate" or "Certification")
    cert_lines = []
    for line in text.splitlines():
        if re.search(r"(Certificate|Certification|Udemy|FutureLearn|HP LIFE)", line, re.IGNORECASE):
            cert_lines.append(line.strip("• ").strip())
    result["Certifications"] = cert_lines

    return result

@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(content={"error": "Only PDF files are supported"}, status_code=400)

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    data = parse_entities(text)
    os.remove(file_path)  # clean up
    return data
