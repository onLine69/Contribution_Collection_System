from flask import render_template, url_for, redirect, request, session
from modules.controller import programCodes, displayContributions, fetchPaid, fetchUnpaid, checkCode, getOrganization, editContributions
from config import ACADEMIC_YEAR
from modules.form import LoginForm
from . import app

# The Homepage
@app.route('/', methods=["GET", "POST"])
def index():
    if 'organization_code' not in session:
        return redirect(url_for('login'))
    else:
        organization_code = session['organization_code']
        program_codes = programCodes(organization_code)
        contributions = displayContributions(organization_code, ACADEMIC_YEAR)
        academic_years = ACADEMIC_YEAR.split("-")
        program_name=None
        chosen_year = None
        selected_month = None
        paid_count = None
        unpaid_count = None

        if request.method == "POST":
            selected_program = request.form.get('programs')
            selected_year = request.form.get('years')
            selected_month = request.form.get('months')

            program_name = selected_program
            selected_month = selected_month
            chosen_year = selected_year

            contribution_name_1 = contributions[0][0]
            contribution_name_2 = contributions[1][0]
            paid_count = { 
                'fcontribution': {
                    'name': contribution_name_1,
                    'data': fetchPaid(contribution_name_1, int(selected_month), selected_program, chosen_year)
                },
                'scontribution': {
                    'name': contribution_name_2,
                    'data': fetchPaid(contribution_name_2, int(selected_month), selected_program, chosen_year)
                }
            }
            print(paid_count)

            unpaid_count = { 
                'fcontribution': {
                    'name': contribution_name_1,
                    'data': fetchUnpaid(selected_program, paid_count['fcontribution']['data'])
                },
                'scontribution': {
                    'name': contribution_name_2,
                    'data': fetchUnpaid(selected_program, paid_count['scontribution']['data'])
                }
            }

        data = {
            'tab_name': "Dashboard"
        }

        return render_template('index.html', 
                            program_codes=program_codes,
                            program_name=program_name,
                            academic_years=academic_years,
                            chosen_year=chosen_year,
                            selected_month = selected_month,
                            paid_count = paid_count,
                            unpaid_count = unpaid_count, 
                            data=data)

@app.route('/profile', methods=["GET", "POST"])
def profile():
    if 'organization_code' not in session:
        return redirect(url_for('login'))
    organization_code = session['organization_code']
    
    if request.method == "POST":
        fname = request.form.get('fcontribution-name')
        famount = request.form.get('fcontribution-amount')
        sname = request.form.get('scontribution-name')
        samount = request.form.get('scontribution-amount')
        editContributions(fname, famount, sname, samount, organization_code)
        return redirect(url_for('profile'))
    
    organization_data = getOrganization(organization_code)
    contribution_data = displayContributions(organization_code, ACADEMIC_YEAR)
    data = {
        'code': organization_data[0],
        'name': organization_data[1],
        'email': organization_data[2],
        'fcon_name': contribution_data[0][0],
        'fcon_amount': contribution_data[0][1],
        'scon_name': contribution_data[1][0],
        'scon_amount': contribution_data[1][1]
    }
    return render_template('profile.html', data=data)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        code = checkCode(request.form.get('code', None))
        if code:
            session['organization_code'] = code
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout', methods=["GET"])
def logout():
    session.pop('organization_code', None)
    return redirect(url_for('index'))
    