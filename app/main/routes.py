from datetime import datetime, timedelta
import os
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from flask import send_from_directory     
from guess_language import guess_language
from app import db
from app.main import bp
from app.models import Transaction
from app.main.forms import MakePayment
from brij.mpesa import MpesaService
from brij.loader import BrijLoader

brij = BrijLoader(app_id=os.environ.get('BRIJ_APP_ID'), app_key=os.environ.get('BRIJ_APP_KEY'))

'''@bp.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 
        'favicon.ico', mimetype='img/logo/favicon-32×32.png')
        '''
        
def validate_mpesa_number(number):
    if number.startswith('+'):
        #remove plus sign
        number = number.replace('+','')
    if number.startswith('0'):
        #replace 0 with 254
        number = '254'+number[1:]
        
    return number

@bp.route('/')
def index():
    form = MakePayment()
    return render_template('index.html', title=_('Make Payments'), payments=form)
    
@bp.route('/request-payment', methods=['POST'])
def request_payment():
    form = MakePayment()
    
    mpesa_number = form.mobile.data
    amount = form.charges.data
    valid_number = validate_mpesa_number(mpesa_number)
    
    # brij direct transaction
    response = brij.get_mpesa_services().mpesa_to_acc(amount, valid_number, valid_number, description='test payment')
    print(response.json())
    
    '''transaction = Transaction(
        amount=amount, 
        phone=validate_mpesa_number
    )
    db.session.add(transaction)
    db.session.commit()'''
    #print(response.json())
    try:
        if response.json()['ResponseCode'] == '0':
            return jsonify(response.text)
    except:
        response.status = 400
        return jsonify(response.json())
    response.status = 400
    return jsonify(response.json())
    
@bp.route('/validate-payment/<merchant_id>', methods=['POST'])
def validate_payment(merchant_id):
    
    response = brij.validate_mpesa_transaction(merchant_id, 'direct')
    print(response.json())
    
    try:
        if response.json()['status']:
            return jsonify(response.text)
    except:
        response.status = 400
        return jsonify(response.json())
    response.status = 400
    return jsonify(response.json())
    
    