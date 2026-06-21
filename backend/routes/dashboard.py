from fastapi import APIRouter
from database import students_collection, marks_collection

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats():
    total_students = students_collection.count_documents({})
    marks_data = list(marks_collection.find())

    if not marks_data:
        return {
            "success": True,
            "total_students": total_students,
            "class_average": 0,
            "top_performer": "No data",
            "top_score": 0,
            "risk_students": 0,
            "leaderboard": [],
            "grade_distribution": {},
            "subject_average": {}
        }

    averages = [m["average"] for m in marks_data]
    class_average = round(sum(averages) / len(averages), 2)

    top = max(marks_data, key=lambda x: x["average"])

    risk_students = len([
        m for m in marks_data
        if m["risk_level"] == "High Risk"
    ])

    grade_distribution = {}
    subject_totals = {}

    for m in marks_data:
        grade = m["grade"]
        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

        for subject, mark in m["subjects"].items():
            subject_totals[subject] = subject_totals.get(subject, 0) + mark

    subject_average = {
        subject: round(total / len(marks_data), 2)
        for subject, total in subject_totals.items()
    }

    leaderboard = sorted(
        [
            {
                "register_number": m["register_number"],
                "average": m["average"],
                "grade": m["grade"],
                "risk_level": m["risk_level"]
            }
            for m in marks_data
        ],
        key=lambda x: x["average"],
        reverse=True
    )[:10]

    return {
        "success": True,
        "total_students": total_students,
        "class_average": class_average,
        "top_performer": top["register_number"],
        "top_score": top["average"],
        "risk_students": risk_students,
        "leaderboard": leaderboard,
        "grade_distribution": grade_distribution,
        "subject_average": subject_average
    }