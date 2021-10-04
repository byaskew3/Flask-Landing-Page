import re
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Champion, User
from market.forms import RegisterForm, LoginForm, PurchaseChampion, SellChampion
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_champion = PurchaseChampion()
    selling_champion = SellChampion()
    if request.method == "POST":
        # Purchased Champion
        purchased_champion = request.form.get('purchased_champion')
        purchase_champion_obj = Champion.query.filter_by(name=purchased_champion).first()
        if purchase_champion_obj:
            if current_user.can_purchase(purchase_champion_obj):
                purchase_champion_obj.buy(current_user)
                flash(f'Congratulations! You purchased {purchase_champion_obj.name} for {purchase_champion_obj.cost} Mana', category='success')
            else:
                flash(f"You don't have enough Mana to purchase {purchase_champion_obj.name}", category='danger')
        # Sold Champion
        sold_champion = request.form.get('sold_champion')
        champion_item_obj = Champion.query.filter_by(name=sold_champion).first()
        if champion_item_obj:
            if current_user.can_sell(champion_item_obj):
                champion_item_obj.sell(current_user)
                flash(f'Congratulations! You sold {champion_item_obj.name} back to the LoL Market!', category='success')
            else:
                flash(f'Something went wrong with selling {champion_item_obj}', category='danger')
        return redirect(url_for('market_page'))

    if request.method == "GET":
        champions = Champion.query.filter_by(owner=None)
        owned_champions = Champion.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=champions, purchase_champion=purchase_champion, owned_champions=owned_champions, selling_champion=selling_champion)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! Welcome to the club {user_to_create.username}!', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}: # no errors from validations
        for err_msg in form.errors.values():
            flash(f'Uh, oh! There was an error creating your account: {err_msg}', category='danger')        
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Welcome {attempted_user.username}!', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password is incorrect!', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You've successfully logged out of LoL Matchup. Come back soon!", category='info')
    return redirect(url_for('home_page'))