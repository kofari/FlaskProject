
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import RegisterForm, LoginForm, DocumentationForm
from app import db
from app.models import User, Documentation

bp = Blueprint('main', __name__)
login_manager = None  # будет заменён в __init__.py

@bp.route('/')
def index():
    docs = Documentation.query.all()
    return render_template('index.html', docs=docs)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_doc():
    form = DocumentationForm()
    if form.validate_on_submit():
        doc = Documentation(title=form.title.data, category=form.category.data, content=form.content.data, created_by=current_user.id)
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('doc_edit.html', form=form)

@bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_authenticated or current_user.email != 'admin@docuhub.com':
        flash('Доступ запрещён')
        return redirect(url_for('main.index'))
    docs = Documentation.query.all()
    users = User.query.all()
    return render_template('admin_panel.html', docs=docs, users=users)

@bp.route('/admin/delete_doc/<int:doc_id>')
@login_required
def delete_doc(doc_id):
    if not current_user.email == 'admin@docuhub.com':
        flash('Недостаточно прав')
        return redirect(url_for('main.index'))
    doc = Documentation.query.get_or_404(doc_id)
    db.session.delete(doc)
    db.session.commit()
    flash('Документ удалён')
    return redirect(url_for('main.admin_panel'))
