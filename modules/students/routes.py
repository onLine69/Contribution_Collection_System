from flask import flash, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from . import students_bp
from modules.students.controller import displayAll, search as searchStudents, add as addStudent, adds, edit as editStudent, customErrorMessages, delete as deleteStudent, fetchUnpaid, fetchPaid, fetchAll
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
                    form.program_code.data,
                    form.note.data
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


@students_bp.route('/student_list', methods=["POST"])
def student_list():
    if 'organization_code' not in session:
        return redirect(url_for('login'))
    
    try:
        req = request.get_json()
        programs = programCodes(req['organization-code'])
        year_levels = ['1', '2', '3', '4']
        data = {
            'list-type': f"{req['type']} Students List",
            'programs': programs,
            'year_levels': year_levels
        }

        for program in programs:
            for year_level in year_levels:
                key = f"{program[0]}-{year_level}"
                match req['type']:
                    case "All":
                        data[key] = fetchAll(program[0], year_level)
                    case "Paid":
                        data[key] = fetchPaid(program[0], year_level)
                    case "Unpaid":
                        data[key] = fetchUnpaid(program[0], year_level)
                    case _:
                        return make_response(jsonify({'message': 'Invalid type.'}), 400)
        
        return jsonify(data)
    except Exception as e:
        return make_response(jsonify({'message': 'Invalid JSON format'}), 400)
