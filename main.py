from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message":"Welcome to FastAPI"}


student_list = []
class Student(BaseModel):
    name:str
    email:str
    phone:int


@app.post("/student")
def student(request:Student):
    student_list.append(request.model_dump())
    return {
        "message":"Student added successfully",
        "student_data":student_list
    }

@app.get("/student/count")
def student_count():
    return {
        "count": len(student_list)
        }