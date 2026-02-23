from fastapi import FastAPI
from models import Student
from database import collection
from bson import ObjectId

app = FastAPI()

# Create Student
@app.post("/students")
def create_student(student: Student):
    result = collection.insert_one(student.dict())
    return {"message": "Student created", "id": str(result.inserted_id)}

# Get All Students
@app.get("/students")
def get_students():
    students = []
    for student in collection.find():
        student["_id"] = str(student["_id"])
        students.append(student)
    return students

# Get Student by ID
@app.get("/students/{id}")
def get_student(id: str):
    student = collection.find_one({"_id": ObjectId(id)})
    if student:
        student["_id"] = str(student["_id"])
        return student
    return {"error": "Student not found"}

# Update Student
@app.put("/students/{id}")
def update_student(id: str, student: Student):
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": student.dict()}
    )
    return {"message": "Student updated"}

# Delete Student
@app.delete("/students/{id}")
def delete_student(id: str):
    collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Student deleted"}