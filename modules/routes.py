from flask import render_template, url_for, redirect, request, session
from modules.controller import programCodes, displayContributions, fetchPaid, fetchUnpaid, checkCode, getOrganization, editContributions
from config import ACADEMIC_YEAR
from . import app

# The Homepage
@app.route('/', methods=["GET", "POST"])
def index():
    if 'organization_code' not in session:
        return redirect(url_for('login'))
    
    organization_code = session['organization_code']
    contributions = displayContributions(organization_code, ACADEMIC_YEAR)

    data = {
        'tab_name': "Dashboard",
        'program_codes': programCodes(organization_code),
        'academic_years': ACADEMIC_YEAR.split("-"),
        'selected_program': None,
        'selected_year': None,
        'selected_month': None
    }

    if request.method == "POST":
        data['selected_program'] = request.form.get('programs')
        data['selected_month'] = request.form.get('months')
        data['selected_year'] = request.form.get('years')

        contribution_name_1 = contributions[0][0]
        contribution_name_2 = contributions[1][0]
        data['paid_count'] = { 
            'fcontribution': {
                'name': contribution_name_1,
                'data': fetchPaid(contribution_name_1, int(data['selected_month']), data['selected_program'], data['selected_year'])
            },
            'scontribution': {
                'name': contribution_name_2,
                'data': fetchPaid(contribution_name_2, int(data['selected_month']), data['selected_program'], data['selected_year'])
            }
        }

        data['unpaid_count'] = { 
            'fcontribution': {
                'name': contribution_name_1,
                'data': fetchUnpaid(data['selected_program'], data['paid_count']['fcontribution']['data'])
            },
            'scontribution': {
                'name': contribution_name_2,
                'data': fetchUnpaid(data['selected_program'], data['paid_count']['scontribution']['data'])
            }
        }

    return render_template('index.html', data=data)

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
        entered_code = request.form.get('code')
        code = checkCode(entered_code)
        if code:
            session['organization_code'] = code[0]
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout', methods=["GET"])
def logout():
    session.pop('organization_code', None)
    return redirect(url_for('index'))
    