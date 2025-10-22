from fastapi import APIRouter, UploadFile, Form
from app.ai_engine import get_answer_from_material, load_materials_to_vector_store
from app.supabase_client import supabase

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
async def ask_question(question: str = Form(...)):
    answer = get_answer_from_material(question)
    return {"answer": answer}
