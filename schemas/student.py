def studentEntity(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"]
    }
def studentsEntity(students)->list:
    return[studentEntity(student) for student in students]
