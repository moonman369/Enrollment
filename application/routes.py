from application import app, db
from flask import render_template, request, json, Response, flash, redirect, url_for, session
from application.models import User, Courses, Enrollment
from application.forms import LoginForm, RegisterForm
import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', index=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f'You are successfully logged in as {user.first_name}!', 'success')
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect('/index')
        else:
            flash('Sorry, something went wrong :/', 'danger')
            
    return render_template('login.html', title='Login', login=True, form=form)


@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/courses')
@app.route('/courses/')
@app.route('/courses/<string:term>')
def courses(term=f'{datetime.date.today().year}'):
    courseData = Courses.objects.order_by('+courseID')
    print(courseData)
    return render_template('courses.html', courseData=courseData, courses=True, term=term)


@app.route('/register', methods=['POST','GET'])
def register():

    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash(f'You are successfully registered as {user.first_name}!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', register=True, form=form, title='Register')


@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():

    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f'You are already registered to {courseTitle}.', 'danger')
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f'You are successfully enrolled to {courseTitle}!', 'success')

    classes = list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'enrollment', 
            'localField': 'user_id', 
            'foreignField': 'user_id', 
            'as': 'r1'
        }
    }, {
        '$unwind': {
            'path': '$r1', 
            'includeArrayIndex': 'r1_id', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'courses', 
            'localField': 'r1.courseID', 
            'foreignField': 'courseID', 
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'user_id': user_id
        }
    }, {
        '$sort': {
            'courseID': 1
        }
    }
]))

    # term = request.form.get('term')

    return render_template('enrollment.html', enrollment=True, title='Enrollment', classes=classes)


@app.route('/api')
@app.route('/api/<idx>')
def api(idx=None):
    courseData = Courses.objects.order_by('+courseID')
    if idx is None:
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype='application/json')


@app.route('/user')
def user():
    # User(user_id=1, first_name='Ayan', last_name='Maiti', email='mightyayan369@gmail.com', password='a1b2c3d4').save()
    users = User.objects.all()
    print(users)
    return render_template('user.html', users=users)
