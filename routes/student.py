from typing import List

from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException, status
from config.db import connection
from models.student import Student

student = APIRouter()


@student.post('/students', status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):

    inserted_student =  connection.students.students.insert_one(student.dict())

    if inserted_student.inserted_id:
        return {"id": str(inserted_student.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to add student")


@student.get("/students", response_model=List[Student])
async def list_students(country: str = None, age: int = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students = list(connection.students.students.find(query))

    student_models = []
    for student_data in students:
        try:
            student_model = Student(**student_data)
            student_models.append(student_model)
        except Exception as e:
            print(f"Error creating Student model: {e}")

    return student_models


@student.get("/students/{student_id}", response_model=Student)
async def fetch_student(student_id: str):
    student = connection.students.students.find_one({"_id": ObjectId(student_id)})

    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@student.patch("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_id: str, student: Student):
    updated_student = connection.students.students.update_one({"_id": ObjectId(student_id)}, {"$set": student.dict()})

    if updated_student.modified_count > 0:
        return {"message": "Student updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@student.delete("/students/{student_id}", response_model=dict)
async def delete_student(student_id: str):
    deleted_student = connection.students.students.delete_one({"_id": ObjectId(student_id)})

    if deleted_student.deleted_count > 0:
        return {}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
