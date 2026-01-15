from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Ihr Konto ist deaktiviert. Bitte kontaktieren Sie den Administrator.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember.data)
            flash(f'Willkommen zurück, {user.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.dashboard'))
        flash('Ungültige E-Mail oder Passwort.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sie wurden erfolgreich abgemeldet.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('Diese E-Mail-Adresse ist bereits registriert.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            email=form.email.data.lower(),
            name=form.name.data,
            role='pflegekraft'  # Default role
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registrierung erfolgreich! Sie können sich jetzt anmelden.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')
