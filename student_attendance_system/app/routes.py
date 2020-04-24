from flask import request, jsonify, render_template, redirect, url_for,flash,session
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import (RegistrationForm,LoginForm)
from werkzeug.utils import secure_filename
from urllib.parse import urlencode
from app import app,db,bcrypt
from app.models import Student_User,Student_Subject
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
        user = Student_User(id=form.id.data, email=form.email.data,batchid=form.batchid.data, password=hashed_password)
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
        user = Student_User.query.filter_by(email=form.email.data).first()
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

#Attendance Route
@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    return render_template('attendance.html')

@app.route('/attendance/submit', methods=['GET', 'POST'])
@login_required
def attendance_submit():
    sub_name=''
    sub_id=''
    batch_name=''
    roll_no=''
    total_class=''
    attend_class=''
    if request.method == 'POST':
        att_det=request.form.get('att_det')
        users=Student_Subject.query.filter_by(batchid=current_user.batchid).filter_by(student_id=current_user.id).all()
        for user in users:
            if user.subjectname in att_det and user.batchid in att_det and user.att_class<user.tot_class:
                sub_name=user.subjectname
                sub_id=user.subjectid
                batch_name=user.batchid
                roll_no=user.student_id
                user.att_class=user.att_class+1
                attend_class=user.att_class
                total_class=user.tot_class
                db.session.commit()
            if user.batchid not in att_det:
                flash("Your attendance can't be taken!", 'danger')
                return redirect(url_for('home'))
    return render_template('attendance_recorded.html',sub_name=sub_name,sub_id=sub_id,batch_name=batch_name,roll_no=roll_no,attend_class=attend_class,total_class=total_class)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    subjects=Student_Subject.query.filter_by(batchid=current_user.batchid).all()
    return render_template('report.html',subjects=subjects)