from flask import Flask, render_template, request, redirect, session, url_for, flash
from models import db, User, Group, Membership, Availability
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def generate_group_code():
    while True:
        code = ''.join(random.choices(string.digits, k=5))
        if not Group.query.filter_by(code=code).first():
            return code

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('User already exists.')
            return redirect('/register')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            session['user_id'] = user.id
            return redirect('/dashboard')
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    user = User.query.get(session['user_id'])
    groups = [m.group for m in user.memberships]
    return render_template('dashboard.html', groups=groups, email=user.email)

@app.route('/create', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        name = request.form['group_name']
        code = generate_group_code()
        group = Group(name=name, code=code)
        db.session.add(group)
        db.session.commit()

        user = User.query.get(session['user_id'])
        membership = Membership(user_id=user.id, group_id=group.id)
        db.session.add(membership)
        db.session.commit()

        print(f"Email sent to {user.email}: Group code is {code}")
        return render_template('invite.html', code=code)
    return render_template('create_group.html')

@app.route('/join', methods=['GET', 'POST'])
def join_group():
    if request.method == 'POST':
        code = request.form['code']
        group = Group.query.filter_by(code=code).first()
        if not group:
            return render_template('join_group.html', error="Invalid Code")
        user = User.query.get(session['user_id'])
        if not Membership.query.filter_by(user_id=user.id, group_id=group.id).first():
            membership = Membership(user_id=user.id, group_id=group.id)
            db.session.add(membership)
            db.session.commit()
        return render_template('join_group.html', success="You have joined the group!")
    return render_template('join_group.html')

@app.route('/group/<code>')
def view_group(code):
    group = Group.query.filter_by(code=code).first_or_404()
    user_ids = [m.user_id for m in group.memberships]
    users = User.query.filter(User.id.in_(user_ids)).all()
    avail_map = {u.id: Availability.query.filter_by(user_id=u.id, group_id=group.id).all() for u in users}

    common = []
    first_user_avails = avail_map[users[0].id] if users else []
    for a in first_user_avails:
        if all(any(b.start == a.start and b.end == a.end for b in avail_map[u.id]) for u in users[1:]):
            common.append(a)

    return render_template('group.html', group=group, common=common)

@app.route('/group/<code>/update', methods=['GET', 'POST'])
def update_group(code):
    group = Group.query.filter_by(code=code).first_or_404()
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        Availability.query.filter_by(user_id=user.id, group_id=group.id).delete()
        starts = request.form.getlist('start')
        ends = request.form.getlist('end')
        for s, e in zip(starts, ends):
            start = datetime.strptime(s, '%Y-%m-%dT%H:%M')
            end = datetime.strptime(e, '%Y-%m-%dT%H:%M')
            a = Availability(user_id=user.id, group_id=group.id, start=start, end=end)
            db.session.add(a)
        db.session.commit()
        return redirect(url_for('view_group', code=code))
    user_avails = Availability.query.filter_by(user_id=user.id, group_id=group.id).all()
    return render_template('update_availability.html', group=group, availabilities=user_avails)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
