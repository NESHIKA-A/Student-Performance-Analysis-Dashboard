from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from database import marks_collection

router = APIRouter(prefix="/marks", tags=["Marks"])


class Marks(BaseModel):
    register_number: str
    python: int
    java: int
    dbms: int
    ai: int
    data_science: int
    maths: int


def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    return "F"


def risk_level(avg):
    if avg >= 75:
        return "Low Risk"
    elif avg >= 50:
        return "Medium Risk"
    return "High Risk"


@router.post("/add")
def add_marks(marks: Marks):
    subjects = {
        "Python": marks.python,
        "Java": marks.java,
        "DBMS": marks.dbms,
        "AI": marks.ai,
        "Data Science": marks.data_science,
        "Maths": marks.maths
    }

    total = sum(subjects.values())
    average = round(total / len(subjects), 2)
    grade = calculate_grade(average)
    risk = risk_level(average)

    weak_subjects = [s for s, m in subjects.items() if m < 50]
    strong_subjects = [s for s, m in subjects.items() if m >= 80]

    marks_collection.insert_one({
        "register_number": marks.register_number,
        "subjects": subjects,
        "total": total,
        "average": average,
        "grade": grade,
        "risk_level": risk,
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects,
        "created_at": datetime.utcnow()
    })

    return {
        "success": True,
        "message": "Marks added successfully",
        "analysis": {
            "total": total,
            "average": average,
            "grade": grade,
            "risk_level": risk,
            "weak_subjects": weak_subjects,
            "strong_subjects": strong_subjects
        }
    }


@router.get("/all")
def get_all_marks():
    data = []

    for item in marks_collection.find():
        data.append({
            "id": str(item["_id"]),
            "register_number": item["register_number"],
            "subjects": item["subjects"],
            "total": item["total"],
            "average": item["average"],
            "grade": item["grade"],
            "risk_level": item["risk_level"],
            "weak_subjects": item["weak_subjects"],
            "strong_subjects": item["strong_subjects"]
        })

    return {"success": True, "marks": data}