from flask import request, jsonify, render_template, redirect, url_for,flash,session
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import (RegistrationForm,LoginForm)
from werkzeug.utils import secure_filename
from urllib.parse import urlencode
from app import app,db,bcrypt
from app.models import User,Subject,Student_Subject,Student_User
import os,time,sys
import qrcode
import datetime

#Home page
@app.route('/')
def home():
    return render_template('index.html')

#REGISTER ROUTE
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(id=form.id.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created succesfully !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

#LOGIN ROUTE
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#LOGOUT ROUTE
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#ADD SUBJECT
@app.route('/add-subject', methods=['GET', 'POST'])
@login_required
def addsubject():
    if request.method == 'POST':
        sub_id=request.form.get('subid')
        sub_name=request.form.get('subname')
        batch_id=request.form.get('batchid')
        subject_det = Subject(subjectid=sub_id,subjectname=sub_name,batchid=batch_id,author=current_user)
        db.session.add(subject_det)
        db.session.commit()
        students=Student_User.query.all()
        for student in students:
            if(student.batchid==batch_id):
                student_subject_det=Student_Subject(subjectid=sub_id,subjectname=sub_name,batchid=batch_id,author=student)
                db.session.add(student_subject_det)
                db.session.commit()
    user = User.query.filter_by(id=current_user.id).first_or_404()
    subjects = Subject.query.filter_by(user_id=user.id).all()
    return render_template('subject.html',subjects=subjects)

# Remove files
# def remove():
#     directory = "app\static\qrcodes"
#     for filename in os.listdir(directory):
#         if filename.endswith(".png"):
#             path=directory+'\\'+filename
#             time_file = os.path.getmtime(path)
#             time_file_time=datetime.datetime.fromtimestamp(time_file)
#             time_now=datetime.datetime.now()
#             time_now_sec=datetime.datetime.now().second
#             if (time_now.minute>time_file_time.minute or time_now.date() > time_file_time.date()) or (time_now_sec-time_file_time.second>=59):
#                 os.remove(path)

#Attendance Route
@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    data=""
    picture_path=""
    imgname=""
    if request.method == 'POST':
        data=request.form.get('options')
        qr=qrcode.QRCode(
            version=1,
            box_size=15,
            border=5
        )
        qr.add_data(data)
        qr.make(fit=True)
        img=qr.make_image(fill='black',back_color='white')
        imgname=data+'.png'
        picture_path = os.path.join(app.root_path, 'static/qrcodes',imgname)
        img.save(picture_path)
    user = User.query.filter_by(id=current_user.id).first_or_404()
    subjects = Subject.query.filter_by(user_id=user.id).all()
    det=""
    for subject in subjects:
        if subject.batchid in data and subject.subjectname in data:
            det=subject.subjectname+" "+subject.batchid
            users=Student_Subject.query.filter_by(batchid=subject.batchid).filter_by(subjectid=subject.subjectid).all()
            for user in users:
                user.tot_class=user.tot_class+1
                db.session.commit()
    # remove()
    return render_template('attendance.html',subjects=subjects,det=det,imgname=imgname)

@app.route('/developers', methods=['GET', 'POST'])
def developers():
    return render_template('developers.html')