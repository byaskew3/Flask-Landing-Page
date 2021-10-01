from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from market.models import Champion, User
from market.forms import RegisterForm
from market import db

@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    champions = Champion.query.all()
    return render_template('market.html', items=champions)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: # no errors from validations
        for err_msg in form.errors.values():
            flash(f'Uh, oh! There was an error creating your account: {err_msg}', category='danger')        
    return render_template('register.html', form=form)