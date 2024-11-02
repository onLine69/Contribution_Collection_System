from flask import flash, render_template, request, redirect, url_for, flash
from . import transactions_bp
from modules.transactions.controller import displayAll, search as searchTransactions
from modules.controller import programCodes, displayContributions, searchContributions
from modules import mysql
from config import ACADEMIC_YEAR


@transactions_bp.route('/', methods=["GET"])
def index():
    contributions = displayContributions("CCS-EC", ACADEMIC_YEAR)
    request_contribution = request.args.get('contribution-names', contributions[0][0], type=str)

    data = {
        'tab_name': "Transaction History",
        'contributions': contributions,
        'chosen_contribution': searchContributions('name', request_contribution, "CCS-EC", ACADEMIC_YEAR)[0],
        'display_program_code': request.args.get('program-code', None, type=str),
        'display_year_level': request.args.get('year-level', None, type=str),
        'display_selected_status': request.args.get('display-status', 'All', type=str),
        'program_codes': programCodes("CCS-EC"),
        'from_point': request.args.get('from-point', None),
        'to_point': request.args.get('to-point', None)
    }
    data['transactions'] = displayAll(data['chosen_contribution'][0], 
                              ACADEMIC_YEAR, 
                              data['display_selected_status'], 
                              data['display_program_code'], 
                              data['display_year_level'], 
                              data['from_point'], 
                              data['to_point'])
    data['count'] = len(data['transactions'])
    
    return render_template('transactions/transactions.html', data=data)


@transactions_bp.route('/search', methods=["GET"])
def search():
    try:
        #fetch the parameters
        column = request.args.get('column-search', 'full_name', type=str)
        searched = request.args.get('param-search', None, type=str)
        
        if searched:
            contributions = displayContributions("CCS-EC", ACADEMIC_YEAR)
            request_contribution = request.args.get('contribution-names', contributions[0][0], type=str)

            data = {
                'tab_name': "Transaction History",
                'column': column,
                'searched': searched,
                'contributions': contributions,
                'chosen_contribution': searchContributions('name', request_contribution, "CCS-EC", ACADEMIC_YEAR)[0],
                'display_program_code':None,
                'display_year_level': None,
                'display_selected_status': None,
                'program_codes': programCodes("CCS-EC"),
                'from_point': None,
                'to_point': None
            }
            
            data['transactions'] = searchTransactions(data['column'], 
                                                      data['searched'], 
                                                      data['chosen_contribution'][0], 
                                                      ACADEMIC_YEAR)
            data['count'] = len(data['transactions'])

            return render_template('transactions/transactions.html', data=data)
    except mysql.connection.Error as e:
        flash(e, "danger")

    return redirect(url_for('transactions.index'))  #if the searched parameter is empty, redirect to the index
