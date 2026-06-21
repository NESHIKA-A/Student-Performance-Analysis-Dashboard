from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv(dotenv_path="../.env")

router = APIRouter(prefix="/ai", tags=["AI Advisor"])

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


class AIRequest(BaseModel):
    student_name: str
    average: float
    grade: str
    risk_level: str
    weak_subjects: list[str]
    strong_subjects: list[str]


@router.post("/study-plan")
def generate_study_plan(data: AIRequest):
    prompt = f"""
You are an expert Academic Performance Advisor.

Analyze the following student details and generate a personalized study plan.

Student Name: {data.student_name}

Current Average: {data.average}%

Current Grade: {data.grade}

Risk Level: {data.risk_level}

Weak Subjects:
{', '.join(data.weak_subjects) if data.weak_subjects else 'None'}

Strong Subjects:
{', '.join(data.strong_subjects) if data.strong_subjects else 'None'}

Provide:

1. Performance Summary
2. Subject-wise Improvement Plan
3. Daily Study Timetable
4. Weekly Study Strategy
5. Exam Preparation Tips
6. Estimated Grade Improvement
7. Motivational Advice

Keep the response professional and concise.
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return {
            "success": True,
            "ai_response": response.text
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }