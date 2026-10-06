from pydantic import BaseModel, Field


class student_get(BaseModel):
    # defining fields with standard python types
    roll_number : int
    name : str
    class_number : int
    age : int
    physics : float
    chemistry : float

class student_post(BaseModel):
    roll_number : int
    name : str
    class_number : int
    age : int
    physics : float
    chemistry : float

class student_update(BaseModel):
    roll_number : int
    parameter : str
    parameter_value : str | int | float

class student_search(BaseModel):
    parameter : str
    value : str | int | float