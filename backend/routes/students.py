from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from database import students_collection

router = APIRouter(prefix="/students", tags=["Students"])


class Student(BaseModel):
    name: str
    register_number: str
    department: str
    year: str
    semester: str
    email: str
    phone: str


@router.post("/add")
def add_student(student: Student):
    existing = students_collection.find_one({
        "register_number": student.register_number
    })

    if existing:
        return {"success": False, "message": "Student already exists"}

    students_collection.insert_one({
        "name": student.name,
        "register_number": student.register_number,
        "department": student.department,
        "year": student.year,
        "semester": student.semester,
        "email": student.email,
        "phone": student.phone,
        "created_at": datetime.utcnow()
    })

    return {"success": True, "message": "Student added successfully"}


@router.get("/all")
def get_students():
    students = []

    for student in students_collection.find():
        students.append({
            "id": str(student["_id"]),
            "name": student["name"],
            "register_number": student["register_number"],
            "department": student["department"],
            "year": student["year"],
            "semester": student["semester"],
            "email": student["email"],
            "phone": student["phone"]
        })

    return {"success": True, "students": students}


@router.get("/count")
def count_students():
    count = students_collection.count_documents({})
    return {"success": True, "total_students": count}