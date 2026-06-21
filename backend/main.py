from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
from routes import auth, students, marks, dashboard, ai

app = FastAPI(title="Student Performance Analysis Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(marks.router)
app.include_router(dashboard.router)
app.include_router(ai.router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Student Performance Analysis Dashboard Backend Running"
    }

@app.get("/test-db")
def test_db():
    db.command("ping")
    return {"message": "✅ MongoDB Atlas Connected Successfully"}