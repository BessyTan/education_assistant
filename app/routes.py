from fastapi import APIRouter, UploadFile, Form
from app.ai_engine import get_answer_from_material, load_materials_to_vector_store
from app.supabase_client import supabase

from app.database_helpers import log_question_answer

router = APIRouter()

@router.post("/upload/")
async def upload_material(file: UploadFile):
    file_bytes = await file.read()
    file_path = f"{file.filename}"
    
    # Upload file to Supabase Storage
    supabase.storage.from_("materials").upload(file_path, file_bytes)
    
    # Store metadata in Supabase database (optional)
    supabase.table("materials").insert({"filename": file.filename}).execute()
    
    text = file_bytes.decode("utf-8")
    load_materials_to_vector_store(text)
    
    return {"message": "File uploaded and processed successfully.", "filename": file.filename}

@router.post("/ask/")
async def ask_question(question: str = Form(...), user_id: str = Form(...)):
    answer = get_answer_from_material(question)

    # Log interaction to Supabase
    log_question_answer(user_id=user_id, question=question, answer=answer)
    
    return {"answer": answer}
