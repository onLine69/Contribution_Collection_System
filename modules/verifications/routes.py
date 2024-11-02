from flask import flash, render_template, request, redirect, url_for, flash, session
from . import verifications_bp
from modules.verifications.controller import displayAll, search as searchPending, verifyTransactions
from modules.verifications.forms import VerificationForm
from modules.controller import displayContributions, searchContributions, programCodes
from config import ACADEMIC_YEAR
from modules import mysql
import datetime
import pdfkit

@verifications_bp.route('/', methods=["GET"])
def index():
    form = VerificationForm()

    contributions = displayContributions("CCS-EC", ACADEMIC_YEAR)
    request_contribution = request.args.get('contribution-names', contributions[0][0])
    
    data = {
        'tab_name': "Verify Payments",
        'contributions': contributions,
        'chosen_contribution': searchContributions('name', request_contribution, "CCS-EC", ACADEMIC_YEAR)[0],
        'display_program_code': request.args.get('program-code', None, type=str),
        'display_year_level': request.args.get('year-level', None, type=str),
        'program_codes': programCodes("CCS-EC")
    }

    data['verifications'] = displayAll(data['chosen_contribution'][0], 
                               ACADEMIC_YEAR, 
                               data['display_program_code'], 
                               data['display_year_level'])
    data['count'] = len(data['verifications'])

    return render_template('verifications/verifications.html',form=form, data=data)


@verifications_bp.route('/search', methods=["GET"])
def search():
    form = VerificationForm()

    column = request.args.get('column-search', 'full_name', type=str)
    searched = request.args.get('param-search', None, type=str)

    try:
        if searched:
            contributions = displayContributions("CCS-EC", ACADEMIC_YEAR)
            request_contribution = request.args.get('contribution-names', contributions[0][0])
            
            data = {
                'tab_name': "Verify Payments",
                'column': column,
                'searched': searched,
                'contributions': contributions,
                'chosen_contribution': searchContributions('name', request_contribution, "CCS-EC", ACADEMIC_YEAR)[0],
                'display_program_code': None,
                'display_year_level': None,
                'program_codes': programCodes("CCS-EC")
            }

            data['verifications'] = searchPending(data['column'], 
                                          data['searched'], 
                                          data['chosen_contribution'][0], 
                                          ACADEMIC_YEAR)
            data['count'] = len(data['verifications'])

            return render_template('verifications/verifications.html', form=form, data=data)
    except mysql.connection.Error as e:
        flash(e, "danger")

    return redirect(url_for('verifications.index'))  #if the searched parameter is empty, redirect to the index

@verifications_bp.route('/verify', methods=["POST"])
def verify():
    try:
        form = VerificationForm(request.form)

        contribution_value = request.form.get('contribution_amount', 0)

        data = {
            'contribution_name': form.contribution_name.data,
            'block_rep': form.block_rep.data,
            'verification_date': str(datetime.datetime.now()).split(" ")[0],
            'program_code': form.program_code.data,
            'year_level': form.year_level.data,
            'total_amount': form.total_amount.data,
            'student_ids': request.form.getlist('student_id'),
            'student_names': request.form.getlist('student_name'),
            'notes': request.form.getlist('transaction_message'),
            'academic_year': ACADEMIC_YEAR
        }
        data['count'] = len(data['student_ids'])
        verifyTransactions(data['contribution_name'], ACADEMIC_YEAR, contribution_value, data['student_ids'], data['notes'])
        return render_template('verifications/receipt.html', data=data)

    except mysql.connection.Error as e:
        flash("Database error: " + str(e), "danger")
    except Exception as ev:
        flash("An error occurred: " + str(ev), "danger")

    return redirect(url_for('verifications.index'))
    
    