# AI-Driven Education Assistant (Supabase Edition)

An **AI-powered adaptive learning assistant** that helps students learn smarter.  
Upload study materials, ask questions in natural language, and get personalized, context-aware responses.  
Built using **FastAPI**, **OpenAI GPT**, and **Supabase** for storage and authentication.

---

## Features

**AI-Powered Q&A** – Ask questions from your uploaded course materials.  
**Supabase Integration** – Secure cloud backend for data and file management.  
**Adaptive Learning** – Tracks topics to provide progressively challenging content (planned).  
**Quiz Generator** – Automatically creates quizzes from uploaded text (planned).  
**Scalable API** – FastAPI backend ready for deployment on Render, Vercel, or AWS.

---

##  Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | FastAPI |
| Database & Auth | Supabase |
| File Storage | Supabase Storage |
| AI / NLP | OpenAI GPT-5 / LangChain |
| Embeddings | FAISS + OpenAI Embeddings |
| Environment | Python 3.10+ |
| Deployment | Render / Docker / Railway |

---

## Project Structure
ai-education-assistant/
│
├── main.py
├── requirements.txt
├── .env.example
│
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── ai_engine.py
│ ├── supabase_client.py
│ └── utils.py
│
├── data/
│ └── faiss_index/
│
├── tests/
│ ├── test_api.py
│ └── test_ai_logic.py
│
└── docs/
  ├── architecture_diagram.png
  ├── api_endpoints.md
  └── project_overview.md

Create Virtual Environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows


Install Dependencies
pip install -r requirements.txt


Configure Environment Variables
.env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=https://your-supabase-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key
SUPABASE_BUCKET=materials

Run the Application
uvicorn main:app --reload
Then open your browser at:
http://127.0.0.1:8000/docs
 to explore the API documentation.


Example Endpoints
➕ Upload Material

POST /upload/
Upload a study material file to Supabase Storage and process it for AI understanding.

Request

curl -X POST "http://127.0.0.1:8000/upload/" \
  -F "file=@materials.txt"


Response
{
  "message": "File uploaded and processed successfully.",
  "filename": "materials.txt"
}



Ask a Question
POST /ask/
Request

curl -X POST "http://127.0.0.1:8000/ask/" \
  -F "question=Explain the concept of neural networks."


Response
{
  "answer": "Neural networks are computational models inspired by the human brain..."
}


Local Development
Run API locally for development:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Test API endpoints with:
pytest


How to Apply the Schema
Go to your Supabase Project → SQL Editor
Copy and paste the contents of supabase_schema.sql
Click Run to initialize the database schema
Verify the new tables appear under the Database → Tables section:
users
materials
progress
logs