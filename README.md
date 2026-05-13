# Resume Parser ATS
Core Language
Python

Used for:

Resume parsing
NLP processing
Backend API
Machine learning workflows
Data preprocessing

Natural Language Processing (NLP)
The project uses NLP techniques to analyze resume content and extract structured information.

NLP Tasks
Tokenization
Named Entity Recognition (NER)
Stop-word removal
Text normalization
Skill extraction
Keyword matching
Resume classification

Machine Learning
Machine learning can be used for:

Resume ranking
ATS scoring
Candidate-job matching
Skill prediction

Python Libraries
spaCy

Used for:
-  Named Entity Recognition (NER)
-  Resume entity extraction
-  NLP pipelines
-  Text preprocessing

Extracted Information
-  Names
-  Skills
-  Organizations
-  Education
-  Experience

NLTK
Used for:

-  Tokenization
-  Stop-word removal
-  Text cleaning

Scikit-learn
Used for:

-  TF-IDF vectorization
-  Similarity scoring
-  Candidate ranking
-  Machine learning models

Common Components
-  TfidfVectorizer
-  CosineSimilarity
-  train_test_split

PyPDF2 / pdfplumber
Used for:

Extracting text from PDF resumes

Pandas
Used for:

-  Data handling
-  CSV processing
-  Candidate datasets

NumPy
Used for:

-  Numerical computations
-  Vector operations
-  Backend

FastAPI:
FastAPI powers the backend API.

Responsibilities
Resume upload handling
ATS score calculation
Resume parsing
Returning extracted data as JSON

Example Endpoint
@app.post("/upload-resume")
def upload_resume():

Uvicorn
ASGI server used to run FastAPI.

Start backend server
uvicorn main:app --reload

Frontend
Frontend can be developed using:

-  HTML
-  CSS
-  JavaScript / TypeScript
-  React + Vite

Frontend Features
-  Resume upload interface
-  ATS score visualization
-  Extracted skills display
-  Candidate dashboard
-  Job description matching
-  Real-time parsing results

REST API Communication
Frontend communicates with FastAPI through REST APIs.

Example
fetch("http://127.0.0.1:8000/upload-resume")

ATS Functionality
The ATS engine evaluates resumes by:

-  Matching resume keywords with job descriptions
-  Calculating similarity scores
-  Ranking candidates
-  Identifying missing skills
-  Generating ATS compatibility scores
