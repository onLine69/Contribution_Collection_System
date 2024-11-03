from flask import flash, render_template, request, redirect, url_for, flash, session
from . import students_bp
from modules.students.controller import displayAll, search as searchStudents, add as addStudent, adds, edit as editStudent, customErrorMessages, delete as deleteStudent
from modules.students.forms import StudentForm
from modules.controller import programCodes
from modules import mysql

@students_bp.route('/', methods=["GET", "POST"])
def index():
    if 'organization_code' not in session:
        return redirect(url_for('login'))
    
    organization_code = session['organization_code']
    form = StudentForm()
    form.program_code.choices = [(program[0], program[0]) for program in programCodes(organization_code)]
    
    students = displayAll()
    data = {
        'tab_name': "Student Records",
        'students': students,
        'count': len(students)
    }
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # Check if the student id is present (editing) or not (adding)
                student_id = request.form.get('student-id', type=str)
                
                student = (
                    form.full_name.data,
                    form.id_number.data,
                    form.gender.data,
                    form.year_level.data,
                    form.program_code.data
                )

                if student_id:
                    student = student + (student_id,)
                    editStudent(student)
                    flash(f"Student {student[0]} has been updated.", "success")
                else:  # We are adding a new student
                    addStudent(student)  # Implement this function to add a new student
                    flash(f"Student {student[0]} has been added.", "success")
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Something is invalid, check the form again.", "warning")

    return render_template('students/students.html', form=form, data=data)


@students_bp.route('/bulk-add', methods=["POST"])
def bulkAdd():
    if request.method == "POST":
        try:
            file = request.files['file-upload']
            adds(file.filename)
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")
    return redirect(url_for('students.index'))


@students_bp.route('/search', methods=["GET"])
def search():
    if 'organization_code' not in session:
        return redirect(url_for('login'))
    
    organization_code = session['organization_code']
    try:
        #fetch the parameters
        column_name = request.args.get('column-search', 'student_id', type=str)
        searched_item = request.args.get('param-search', None, type=str)

        if searched_item:
            # Fetch the students
            form = StudentForm()
            form.program_code.choices = [(program[0], program[0]) for program in programCodes(organization_code)]
            
            students = searchStudents(column_name, searched_item)

            data = {
                'tab_name': "Student Records",
                'column': column_name,
                'searched': searched_item,
                'students': students,
                'count': len(students)
            }
                    
            return render_template('students/students.html', form=form, data=data)
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")

    return redirect(url_for('students.index'))  #if the searched parameter is empty, redirect to the index


@students_bp.route('/delete/<id_number>', methods=["POST"])
def delete(id_number):
    try:
        deleteStudent(id_number)
        flash(f"Student '{id_number}' removed successfully!", "success")
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
    
    return redirect(url_for('students.index'))