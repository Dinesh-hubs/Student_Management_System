from fastapi import FastAPI,HTTPException
from database import *
from models import *

# initialization of the application 

app = FastAPI()

@app.get("/")
def home():
    return {"Message : Welcome to Student Management System. Please type /docs to interact with the program."}

# creating the path
@app.get("/get_students/",response_model= list[student_get])
def get_students():
    students = get_all_students()
    result = []
    for student in students:
        converted_student = student_get(
            roll_number = student[0],
            name = student[1],
            class_number = student[2],
            age = student[3],
            physics = student[4],
            chemistry = student[5]
        )
        result.append(converted_student)
    return result


def pretty_print(student_data):
    if not student_data:
        return
    converted_student = student_get(
        roll_number = student_data[0],
        name = student_data[1],
        class_number = student_data[2],
        age = student_data[3],
        physics = student_data[4],
        chemistry = student_data[5]
    )
    return converted_student

@app.post("/post_student", response_model = student_get)
def add_student(student : student_post):
    insert_student(student.roll_number,student.name,student.class_number,student.age,student.physics,student.chemistry)
    std = get_student_by_rno(student.roll_number)
    pretty_std = pretty_print(std)
    return pretty_std


@app.patch("/update_student", response_model = student_get)
def update_std(student : student_update):

    allowed_parameters = {
        "name" : str,
        "class_number" : int,
        "age" : int,
        "physiics" : float,
        "chemistry" : float
    }

    if student.parameter not in allowed_parameters:
        raise HTTPException(status_code=400, detail = "Invalid Parameter")

    expected_type = allowed_parameters[student.parameter]

    if not isinstance(student.parameter, expected_type):
        raise HTTPException(status_code = 400, detail = f"{student.parameter} must be of type {expected_type.__name__}")

    update_student(student.roll_number,student.parameter,student.parameter_value)

    updated_student = get_student_by_rno(student.roll_number)
    pretty_std = pretty_print(updated_student)

    return pretty_std

@app.delete("/delete_student/{roll_number}")
def remove_student(roll_number : int):
    student = get_student_by_rno(roll_number)

    if not student:
        raise HTTPException(status_code= 404, detail= "Student not found")

    delete_student(roll_number)

    return {
        "message" : "Student data removed successfully.",
        "roll number" : roll_number
    }