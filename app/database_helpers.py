"""
app/database_helpers.py
───────────────────────────────
Utility functions for interacting with the Supabase database.
Handles inserting and retrieving user logs, materials, and progress data.
"""

from datetime import datetime
from app.supabase_client import supabase


# ─────────────────────────────────────────────
# Function: log_question_answer
# Logs user interactions (questions and AI answers) into Supabase
# ---------------------------------------------------------------
def log_question_answer(user_id: str, question: str, answer: str) -> None:
    """
    Inserts a record into the Supabase 'logs' table for analytics.
    """
    try:
        data = {
            "user_id": user_id,
            "question": question,
            "answer": answer,
            "created_at": datetime.utcnow().isoformat(),
        }
        response = supabase.table("logs").insert(data).execute()
        if response.data:
            print(f"Logged question for user {user_id}")
        else:
            print("Log insertion returned no data.")
    except Exception as e:
        print(f"Error logging question-answer pair: {e}")


# ─────────────────────────────────────────────
# Function: get_user_logs
# Retrieves a user’s Q&A history from the database
# ---------------------------------------------------------------
def get_user_logs(user_id: str, limit: int = 10):
    """
    Returns the last `limit` question/answer logs for a specific user.
    """
    try:
        response = (
            supabase.table("logs")
            .select("question, answer, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []


# ─────────────────────────────────────────────
# Function: update_user_progress
# Stores or updates user progress metrics
# ---------------------------------------------------------------
def update_user_progress(user_id: str, topic: str, score: int):
    """
    Inserts or updates the user's progress for a specific topic.
    """
    try:
        existing = (
            supabase.table("progress")
            .select("id, attempts, score")
            .eq("user_id", user_id)
            .eq("topic", topic)
            .execute()
        )

        if existing.data:
            progress_id = existing.data[0]["id"]
            attempts = existing.data[0]["attempts"] + 1
            avg_score = (existing.data[0]["score"] + score) // 2

            supabase.table("progress").update({
                "attempts": attempts,
                "score": avg_score,
                "last_reviewed": datetime.utcnow().isoformat()
            }).eq("id", progress_id).execute()
        else:
            supabase.table("progress").insert({
                "user_id": user_id,
                "topic": topic,
                "score": score,
                "attempts": 1
            }).execute()
    except Exception as e:
        print(f"Error updating progress: {e}")
