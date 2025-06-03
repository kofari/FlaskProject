
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import RegisterForm, LoginForm, DocumentationForm, UpdateProfileForm
from app import db
from app.models import User, Documentation

bp = Blueprint('main', __name__)
login_manager = None  # будет заменён в __init__.py

@bp.route('/')
def index():
    query = request.args.get('q')
    if query:
        docs = Documentation.query.filter(Documentation.title.ilike(f"%{query}%")).all()
    else:
        docs = Documentation.query.all()
    return render_template('index.html', docs=docs)

@bp.route('/doc/<int:doc_id>')
def view_doc(doc_id):
    doc = Documentation.query.get_or_404(doc_id)
    return render_template('doc_view.html', doc=doc)

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

@bp.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    docs = Documentation.query.filter_by(created_by=user.id).all()
    return render_template('user_profile.html', user=user, docs=docs)

@bp.route('/admin/edit_doc/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def edit_doc(doc_id):
    if current_user.email != "admin@docuhub.com":
        flash("Доступ запрещён")
        return redirect(url_for("main.index"))
    doc = Documentation.query.get_or_404(doc_id)
    form = DocumentationForm(obj=doc)
    if form.validate_on_submit():
        doc.title = form.title.data
        doc.category = form.category.data
        doc.content = form.content.data
        db.session.commit()
        flash("Документация обновлена.")
        return redirect(url_for("main.admin_panel"))
    return render_template("doc_edit.html", form=form)



@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    if current_user.id != user_id:
        flash('Доступ запрещён')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    form = UpdateProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        flash('Профиль обновлён')
        return redirect(url_for('main.user_profile', user_id=user.id))
    return render_template('edit_profile.html', form=form)



@bp.route('/doc/edit/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def user_edit_doc(doc_id):
    doc = Documentation.query.get_or_404(doc_id)
    if doc.created_by != current_user.id:
        flash('Недостаточно прав')
        return redirect(url_for('main.index'))
    form = DocumentationForm(obj=doc)
    if form.validate_on_submit():
        doc.title = form.title.data
        doc.category = form.category.data
        doc.content = form.content.data
        db.session.commit()
        flash('Документация обновлена')
        return redirect(url_for('main.user_profile', user_id=current_user.id))
    return render_template('doc_edit.html', form=form)


@bp.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    # Only admin (by email) can delete users
    if not current_user.is_authenticated or current_user.email != 'admin@docuhub.com':
        flash('Доступ запрещён')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    if user.email == 'admin@docuhub.com':
        flash('Нельзя удалить администратора')
        return redirect(url_for('main.admin_panel'))
    # Delete user's documents first
    docs = Documentation.query.filter_by(created_by=user.id).all()
    for doc in docs:
        db.session.delete(doc)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь и его посты удалены')
    return redirect(url_for('main.admin_panel'))

