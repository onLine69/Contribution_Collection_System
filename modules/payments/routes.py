from flask import flash, render_template, request, redirect, url_for, flash
from . import payments_bp
from modules.payments.controller import displayAll, search as searchStudents, customErrorMessages, fetchPaid, fetchUnpaid, createTransaction
from modules.controller import displayContributions, searchContributions, programCodes
from modules import mysql
from config import ACADEMIC_YEAR

@payments_bp.route('/', methods=["GET", "POST"])
def index():
    contributions = displayContributions("CCS-EC", ACADEMIC_YEAR)
    request_contribution = request.args.get('contribution-names', contributions[0][0], type=str)
    
    data = {
        'tab_name': "Payment Records",
        'contributions': contributions,
        'chosen_contribution': searchContributions('name', request_contribution, "CCS-EC", ACADEMIC_YEAR)[0],
        'display_program_code': request.args.get('program-code', None, type=str),
        'display_year_level': request.args.get('year-level', None, type=str),
        'display_selected_status': request.args.get('display-status', 'All', type=str),
        'program_codes': programCodes("CCS-EC")
    }

    if data['display_selected_status'] == "All":
        paid_students = fetchPaid(request_contribution, data['display_year_level'], data['display_program_code'], ACADEMIC_YEAR)
        data['stat'] = {
            'paid': {
                'data': paid_students
            },
            'unpaid': {
                'data': fetchUnpaid(data['display_year_level'], data['display_program_code'], paid_students)
            }
        }

    data['students'] = displayAll(data['chosen_contribution'][0], 
                                  ACADEMIC_YEAR, 
                                  data['display_selected_status'], 
                                  data['display_program_code'], 
                                  data['display_year_level'])
    
    data['count'] = len(data['students'])

    return render_template('payments/payments.html', data=data)

@payments_bp.route('/search', methods=["GET"])
def search():   # Display the searched student
    #fetch the parameters
    column = request.args.get('column-search', 'full_name', type=str)
    searched = request.args.get('param-search', None, type=str)

    try:
        if searched:
            contributions = displayContributions("CCS-EC", ACADEMIC_YEAR)
            request_contribution = request.args.get('contribution-names', contributions[0][0])

            data = {
                'tab_name': "Payment Records",
                'column': column,
                'searched': searched,
                'contributions': contributions,
                'chosen_contribution': searchContributions('name', request_contribution, "CCS-EC", ACADEMIC_YEAR)[0],
                'display_program_code': None,
                'display_year_level': None,
                'display_selected_status': None,
                'program_codes': programCodes("CCS-EC")
            }

            data['students'] = searchStudents(data['column'], 
                                              data['searched'], 
                                              data['chosen_contribution'][0], 
                                              ACADEMIC_YEAR)
            
            data['count'] = len(data['students'])

            return render_template('payments/payments.html', data=data)
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")

    return redirect(url_for('payments.index'))  #if the searched parameter is empty, redirect to the index


@payments_bp.route('/transact', methods=["POST"])
def transact():
    try:
        selected_ids = request.form.getlist('student-id', type=str)  # Get list of selected checkbox values
        contribution_name = request.form.get('contribution-name', type=str)
        contribution_ay = request.form.get('contribution-ay', type=str)
        contribution_amount = request.form.get('contribution-amount', type=int)
        transaction_messages = request.form.getlist('transaction-message', type=str)

        createTransaction(contribution_name, contribution_ay, contribution_amount, selected_ids, transaction_messages)

    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
    return redirect(url_for('payments.index'))  #if the searched parameter is empty, redirect to the index