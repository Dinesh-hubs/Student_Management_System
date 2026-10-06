import sqlite3

ALLOWED_PARAMETERS = {
    "name",
    "age",
    "class_number",
    "physics",
    "chemistry"
}

def get_connection():    
    return sqlite3.connect("students.db")

def get_all_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    connection.close()

    return students

def insert_student(rno,name,class_num,age,phy,chem):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT EXISTS (SELECT 1 FROM students WHERE roll_number = ?)', (rno,))
    exists = cursor.fetchone()[0]

    if exists:
        connection.close()
        return False
    else:
        cursor.execute("INSERT INTO students (roll_number,name,class_number,age,physics,chemistry) VALUES (?,?,?,?,?,?)",(rno,name,class_num,age,phy,chem))
        connection.commit()
        connection.close()

def update_student(rno,parameter,parameter_value):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT EXISTS (SELECT 1 FROM students WHERE roll_number = ?)', (rno,))
    exists = cursor.fetchone()[0]

    if parameter not in ALLOWED_PARAMETERS:
        raise ValueError("Invalid Parameter.")

    if exists:
        cursor.execute(f"UPDATE students SET {parameter} = ? WHERE roll_number = ?", (parameter_value,rno))
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

def delete_student(rno):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE roll_number = ?",(rno,))

    connection.commit()
    connection.close()

def get_student_by_rno(rno):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE roll_number = ?",(rno,))

    student = cursor.fetchone()

    connection.close()

    return student

def search_student(parameter,value):
    connection = get_connection()
    cursor = connection.cursor()
    parameter = parameter.lower()

    if parameter == "rno":
        connection.close()
        return get_student_by_rno(value)

    elif parameter not in ALLOWED_PARAMETERS :
        raise ValueError("Invalid Parameter")

    if parameter == "name":
        cursor.execute(f"SELECT * FROM students WHERE {parameter} COLLATE NOCASE = ?",(value,))
    else:
        cursor.execute(f"SELECT * FROM students WHERE {parameter} = ?",(value,))

    student = cursor.fetchall()

    connection.close()

    return student

if __name__ == "__main__":
    obj = search_student("physics",67)
    print(obj)