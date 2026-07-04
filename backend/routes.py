from flask import current_app as app
from flask import render_template, redirect, request, flash
from .models import *
from flask_login import login_user, login_required, current_user, logout_user

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        femail = request.form.get("email")
        fpwd = request.form.get("pwd")
        
        user = db.session.query(User).filter_by(email=femail).first()
        
        if user:
            if user.status == 'blacklisted':
                return "Your account has been blacklisted."
            if user.password == fpwd:
                login_user(user)
                if user.role == 'admin':
                    return redirect("/admin/dashboard")
                elif user.role == 'staff':
                
                    staff_profile = db.session.query(StaffProfile).filter_by(user_id=user.id).first()
                    if staff_profile and staff_profile.status == 'approved':
                        return redirect("/staff/dashboard")
                    else:
                        return "Your account is pending admin approval."
                elif user.role == 'trekker':
                    return redirect("/trekker/dashboard")
            else:
                return "Invalid password!"
        else:
            return "User not found!"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return "Admin Dashboard - (will make next)"

@app.route('/staff/dashboard')
@login_required
def staff_dashboard():
    return "Staff Dashboard - (will make next)"

@app.route('/trekker/dashboard')
@login_required
def trekker_dashboard():
    return "Trekker Dashboard - (will make next)"