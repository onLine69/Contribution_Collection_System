from flask import render_template, url_for, redirect, request
from modules.controller import programCodes, displayContributions, fetchPaid, fetchUnpaid
from config import ACADEMIC_YEAR
from . import app

# The Homepage
@app.route('/', methods=["GET", "POST"])
def index():
    program_codes = programCodes("CCS-EC")

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

        contribution_name_1 = "1st Sem Membership Fee"
        contribution_name_2 = "2nd Sem Membership Fee"
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

    print(paid_count)

    return render_template('index.html', 
                           program_codes=program_codes,
                           program_name=program_name,
                           academic_years=academic_years,
                           chosen_year=chosen_year,
                           selected_month = selected_month,
                           paid_count = paid_count,
                           unpaid_count = unpaid_count, 
                           current_tab="Dashboard")