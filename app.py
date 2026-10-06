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


def convert_student(student_data):
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

def pretty_print(student_data):
    if not student_data:
        return []

    result = []

    for student in student_data:
        result.append(convert_student(student))

    return result

@app.post("/post_student", response_model = student_get)
def add_student(student : student_post):
    success = insert_student(student.roll_number,student.name,student.class_number,student.age,student.physics,student.chemistry)
    if not success:
        raise HTTPException(status_code=409, detail = "Student already exists with this roll number.")
    std = get_student_by_rno(student.roll_number)
    pretty_std = convert_student(std)
    return pretty_std


@app.patch("/update_student", response_model = student_get)
def update_std(student : student_update):

    allowed_parameters = {
        "name" : str,
        "class_number" : int,
        "age" : int,
        "physics" : float,
        "chemistry" : float
    }

    if student.parameter not in allowed_parameters:
        raise HTTPException(status_code=400, detail = "Invalid Parameter")

    expected_type = allowed_parameters[student.parameter]

    if not isinstance(student.parameter_value, expected_type):
        raise HTTPException(status_code = 400, detail = f"{student.parameter} must be of type {expected_type.__name__}")

    success = update_student(student.roll_number,student.parameter,student.parameter_value)
    if not success:
        raise HTTPException(status_code= 409, detail = "There is no student with those details.")

    updated_student = get_student_by_rno(student.roll_number)
    pretty_std = convert_student(updated_student)

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

@app.get("/search_student", response_model = list[student_get])
def search_students(parameter : str, value : str):
    allowed_parameters = {
            "name" : str,
            "class_number" : int,
            "age" : int,
            "physics" : float,
            "chemistry" : float
        }

    parameter = parameter.lower()
    
    if parameter not in allowed_parameters:
        raise HTTPException(status_code=400, detail = "Invalid Parameter")

    expected_type = allowed_parameters[parameter]

    try:
        if expected_type == int:
            value = int(value)
        elif expected_type == float:
            value = float(value)
    except ValueError:
            raise HTTPException(status_code = 400, detail = f"{parameter} must be of type {expected_type.__name__}")
        
    d_student = search_student(parameter = parameter, value = value)
    return pretty_print(d_student)
