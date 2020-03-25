from datetime import datetime, timedelta
import os
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from flask import send_from_directory     
from guess_language import guess_language
from app import db
from app.main import bp, helper
from app.models import Transaction
from app.main.forms import MakePayment

@bp.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 
        'favicon.ico', mimetype='img/logo/favicon-32×32.png')
        
def validate_mpesa_number(number):
    if number.startswith('+'):
        #remove plus sign
    if number.startswith('0'):
        #replace 0 with 254
        
    return number

@bp.route('/')
def index():
    form = MakePayment()
    if form.validate_on_submit():
        mpesa_number = form.mobile.data
        amount = form.charges.data
        
        valid_number = validate_mpesa_number(mpesa_number)
        
        #todo brij direct transaction
        
        transaction = Transaction(
            amount=amount, 
            phone=validate_mpesa_number, 
            conductor=current_user.id
        )
        db.session.add(application)
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('index.html', title=_('Make Payments'), payments=form)