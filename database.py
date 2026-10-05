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
        print("There is already a student with the roll number")
        connection.close()
    else:
        cursor.execute("INSERT INTO students (roll_number,name,class_number,age,physics,chemistry) VALUES (?,?,?,?,?,?)",(rno,name,class_num,age,phy,chem))
        connection.commit()
        connection.close()

def update_student(rno,parameter,parameter_value):
    connection = get_connection()
    cursor = connection.cursor()

    if parameter not in ALLOWED_PARAMETERS:
        raise ValueError("Invalid Parameter.")

    cursor.execute(f"UPDATE students SET {parameter} = ? WHERE roll_number = ?", (parameter_value,rno))
    connection.commit()
    connection.close()

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

if __name__ == "__main__":
    obj = insert_student(101,'DD',12,18,90,98)