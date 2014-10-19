from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
	return render_template("get_github.html")

@app.route("/create_student")
def create_student():
	return render_template("create_student.html")

@app.route("/new")
def new_student():
	hackbright_app.connect_to_db()
	student_first = request.args.get('first_name')
	student_last = request.args.get('last_name')
	student_github = request.args.get('github')
	return_string = hackbright_app.make_new_student(student_first, 
		student_last, student_github)
	return render_template("new_student_success.html", return_string = return_string)

@app.route("/create_project")
def create_project():
	return render_template("create_project.html")

@app.route("/new_project")
def new_project():
	hackbright_app.connect_to_db()
	title = request.args.get('title')
	description = request.args.get('description')
	return_string = hackbright_app.make_new_project(title, 
		description)
	return render_template("new_project_success.html", return_string = return_string)

@app.route("/grade_student_form")
def grade_student_form():
	return render_template("grade_student_form.html")


@app.route("/grade_student")
def grade_student():
	hackbright_app.connect_to_db()
	first_name = request.args.get('first_name')
	print first_name
	last_name = request.args.get('last_name')
	project = request.args.get('project')
	grade = int(request.args.get('grade'))
	return_string = hackbright_app.assign_grade(first_name, last_name, 
		grade, project)
	return render_template("add_grade_success.html", return_string = return_string)


@app.route("/student")
def get_student():
	hackbright_app.connect_to_db()
	student_github = request.args.get("github")
	row = hackbright_app.get_student_by_github(student_github)
	grades = hackbright_app.show_grades(row[0], row[1])


	#Initialize an empty dictionary to send this particular students grades
	#to the template
	studentgrades = {}

	#Unpack the project, grade into the dictionary as key, value pairs
	for grade in grades:
		studentgrades[grade[2]] = grade[3]

	html = render_template("student_info.html", first_name=row[0],
		last_name=row[1], github=row[2], grade = studentgrades)

	return html

@app.route("/all_grades")
def get_all_grades():
	hackbright_app.connect_to_db()
	project = request.args.get("project") #get the project from the form
	row = hackbright_app.show_grades_for_project(project)
	grades_dictionary = {}
	i = 0
	while  i in range(len(row)):
		name = row[i][0]+" "+row[i][1]
		
		inner = {}
		inner["name"] = name
		inner["github"] = row[i][2]
		inner["grade"] = row[i][3]

		grades_dictionary[i] = inner
			
		i += 1
	html = render_template("project_grades.html", title = project, grades
		= grades_dictionary)
	return html



if __name__ == "__main__":
	app.run(debug=True)