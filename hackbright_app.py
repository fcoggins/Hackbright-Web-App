import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    # print "Row from HB_app", row
    return row

def get_project_by_title(project):
    query = """SELECT title, description, max_grade FROM projects WHERE title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    print """\
Project Title: %s
Description: %s
Maximum Grade: %s"""%(row[0], row[1], row[2])

def get_students_grade_by_project(first_name, last_name, project):
    query = """SELECT first_name, last_name, project_title, grade 
    FROM students
    JOIN grades
    ON (github = student_github)
    JOIN projects
    ON (title = project_title)
    WHERE first_name = ?
    AND last_name = ?
    AND project_title = ?"""
    DB.execute(query, (first_name, last_name, project))
    row = DB.fetchone()
    print """\
Student: %s %s
Project: %s
Grade: %s"""%(row[0], row[1], row[2], row[3])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    return "Successfully added student: %s %s"%(first_name, last_name)

def assign_grade(first_name, last_name, grade, title):
    query1 = """SELECT github FROM students WHERE first_name = ? and 
    last_name = ?"""
    DB.execute(query1, (first_name, last_name))
    row = DB.fetchone()
    github = row[0]
    query = """INSERT INTO  grades VALUES (?, ?, ?) """
    DB.execute(query, (github, title, grade))
    CONN.commit()
    print "Successfully added %s %s grade for %s project"%(first_name, last_name, title)
    print "The grade entered was %s"%(grade)

def show_grades(first_name, last_name):
    query = """SELECT first_name, last_name, project_title, grade FROM students
    JOIN grades ON (github = student_github)
    WHERE first_name = ?
    AND last_name = ?"""
    DB.execute(query, (first_name, last_name))
    row = DB.fetchall()
    #print row
    return row

def show_grades_for_project(project):
    query = """SELECT first_name, last_name, github, grade 
    FROM students
    JOIN grades
    ON (github = student_github)
    WHERE project_title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchall()
    return row
    

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "projects":
            get_project_by_title(*args)
        elif command == "grade":
            get_students_grade_by_project(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "show_grades":
            show_grades(*args)
        elif command == "show_project_grade":
            show_grades_for_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
