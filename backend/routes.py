from flask import current_app as app
from flask import render_template, redirect, request, flash
from .models import *
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
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

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='GET':
        role=request.args.get('role')
        if role=='trekker':
            return render_template('trekker/register.html')
        elif role=='staff':
            return render_template('staff/register.html')
        else:
            return redirect('/')
    
    if request.method=='POST':
        role=request.args.get('role')
        fname=request.form.get('name')
        femail=request.form.get('email')
        fpwd=request.form.get('pwd')
        fphone=request.form.get('phone')
        faddress=request.form.get('address')

        existing=db.session.query(User).filter_by(email=femail).first()
        if existing:
            return "User with this email already exists."
        
        if role=='trekker':
            new_user = User(
                name=fname,
                email=femail,
                password=fpwd,
                phone=fphone,
                address=faddress,
                role='trekker',
                status='active'
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        
        elif role=='staff':
            fbio = request.form.get('bio')
            fexp = request.form.get('exp_years')
            new_user = User(
                name=fname,
                email=femail,
                password=fpwd,
                phone=fphone,
                address=faddress,
                role='staff',
                status='active'
            )
            db.session.add(new_user)
            db.session.commit()
            new_profile = StaffProfile(
                user_id=new_user.id,
                bio=fbio,
                exp_years=int(fexp),
                status='pending'
            )
            db.session.add(new_profile)
            db.session.commit()
            return redirect('/login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()
    pending_staff = StaffProfile.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings,
        pending_staff=pending_staff
    )
@app.route('/admin/treks')
@login_required
def admin_treks():
    treks = Trek.query.all()
    return render_template('admin/treks.html', treks=treks)

@app.route('/admin/trek/add', methods=['GET', 'POST'])
@login_required
def admin_add_trek():
    if request.method == 'GET':
        return render_template('admin/add_trek.html')
    
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')
        duration = int(request.form.get('duration'))
        total_slots = int(request.form.get('total_slots'))
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()  
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() 
        description = request.form.get('description')

        new_trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            total_slots=total_slots,
            available_slots=total_slots,  
            status='Pending',
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        db.session.add(new_trek)
        db.session.commit()
        return redirect('/admin/treks')

@app.route('/admin/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if request.method == 'GET':
        return render_template('admin/edit_trek.html', trek=trek)
    
    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration = int(request.form.get('duration'))
        trek.total_slots = int(request.form.get('total_slots'))
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')
        trek.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        trek.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        trek.description = request.form.get('description')
        db.session.commit()
        return redirect('/admin/treks')


@app.route('/admin/trek/<int:trek_id>/delete')
@login_required
def admin_delete_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if trek:
        db.session.delete(trek)
        db.session.commit()
    return redirect('/admin/treks')


@app.route('/admin/trek/<int:trek_id>/assign', methods=['GET', 'POST'])
@login_required
def admin_assign_staff(trek_id):
    trek = Trek.query.get(trek_id)
    
    approved_staff = db.session.query(StaffProfile).filter_by(status='approved').all()
    
    if request.method == 'GET':
        return render_template('admin/assign_staff.html', trek=trek, staff_list=approved_staff)
    
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        trek.assigned_staff_id = int(staff_id)
        db.session.commit()
        return redirect('/admin/treks')

@app.route('/admin/staff')
@login_required
def admin_staff():
    staff_list = db.session.query(StaffProfile).all()
    return render_template('admin/staff.html', staff_list=staff_list)

@app.route('/admin/staff/<string:action>/<int:staff_id>')
@login_required
def admin_staff_action(action, staff_id):
    staff = StaffProfile.query.get(staff_id)
    if staff:
        if action == 'approve':
            staff.status = 'approved'
        elif action == 'blacklist':
            staff.status = 'blacklisted'
        elif action == 'unblacklist':
            staff.status = 'approved'
        db.session.commit()
    return redirect('/admin/staff')

@app.route('/admin/users')
@login_required
def admin_users():
    users = User.query.filter_by(role='trekker').all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<string:action>/<int:user_id>')
@login_required
def admin_user_action(action, user_id):
    user = User.query.get(user_id)
    if user:
        if action == 'blacklist':
            user.status = 'blacklisted'
        elif action == 'unblacklist':
            user.status = 'active'
        db.session.commit()
    return redirect('/admin/users')

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    bookings = Booking.query.all()
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/search')
@login_required
def admin_search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'trek')
    results_treks = []
    results_users = []
    results_staff = []

    if query:
        if search_type == 'trek':
            results_treks = Trek.query.filter(
                Trek.name.ilike(f'%{query}%') | Trek.location.ilike(f'%{query}%')
            ).all()
        elif search_type == 'user':
            results_users = User.query.filter(
                User.role == 'trekker',
            ).filter(
                User.name.ilike(f'%{query}%') | User.email.ilike(f'%{query}%')
            ).all()
        elif search_type == 'staff':
            results_staff = User.query.filter(
                User.role == 'staff'
            ).filter(
                User.name.ilike(f'%{query}%') | User.email.ilike(f'%{query}%')
            ).all()

    return render_template('admin/search.html',
        query=query,
        search_type=search_type,
        results_treks=results_treks,
        results_users=results_users,
        results_staff=results_staff
    )


@app.route('/staff/dashboard')
@login_required
def staff_dashboard():
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff_profile.id).all()
    # counting trekkers per trek
    trek_data = []
    for trek in assigned_treks:
        count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        trek_data.append({'trek': trek, 'count': count})
    
    return render_template('staff/dashboard.html',
        staff_profile=staff_profile,
        trek_data=trek_data
    )

@app.route('/staff/trek/<int:trek_id>/update', methods=['GET', 'POST'])
@login_required
def staff_update_trek(trek_id):
    trek = Trek.query.get(trek_id)
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    
    if trek.assigned_staff_id != staff_profile.id:
        return "Unauthorized. You are not assigned to this trek."
    
    if request.method == 'GET':
        return render_template('staff/update_trek.html', trek=trek)
    
    if request.method == 'POST':
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')
        db.session.commit()
        return redirect('/staff/dashboard')

@app.route('/staff/trek/<int:trek_id>/participants')
@login_required
def staff_participants(trek_id):
    trek = Trek.query.get(trek_id)
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    
    if trek.assigned_staff_id != staff_profile.id:
        return "Unauthorized. You are not assigned to this trek."
    
    bookings = Booking.query.filter_by(trek_id=trek_id, status='Booked').all()
    return render_template('staff/participants.html', trek=trek, bookings=bookings)

@app.route('/trekker/dashboard')
@login_required
def trekker_dashboard():
    available_treks = Trek.query.filter_by(status='Open').all()
    my_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    
    return render_template('trekker/dashboard.html',
        available_treks=available_treks,
        my_bookings=my_bookings
    )

@app.route('/trekker/trek/<int:trek_id>/book')
@login_required
def trekker_book_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if trek.status != 'Open':
        return "This trek is not open for booking!"

    if trek.available_slots <= 0:
        return "No slots available for this trek!"

    existing = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek_id,
        status='Booked'
    ).first()
    if existing:
        return "You have already booked this trek!"

    new_booking = Booking(
        user_id=current_user.id,
        trek_id=trek_id,
        status='Booked',
        payment_status='Pending'
    )
    db.session.add(new_booking)

    trek.available_slots -= 1
    db.session.commit()

    return redirect('/trekker/bookings')

@app.route('/trekker/bookings')
@login_required
def trekker_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('trekker/bookings.html', bookings=bookings)

@app.route('/trekker/treks')
@login_required
def trekker_treks():
    difficulty = request.args.get('difficulty', '')
    location = request.args.get('location', '')
    search = request.args.get('search', '')

    query = Trek.query.filter_by(status='Open')

    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    if search:
        query = query.filter(Trek.name.ilike(f'%{search}%'))

    treks = query.all()

    booked_trek_ids = [b.trek_id for b in Booking.query.filter_by(
        user_id=current_user.id, status='Booked').all()]

    return render_template('trekker/treks.html',
        treks=treks,
        difficulty=difficulty,
        location=location,
        search=search,
        booked_trek_ids=booked_trek_ids
    )

@app.route('/trekker/profile/edit', methods=['GET', 'POST'])
@login_required
def trekker_edit_profile():
    if request.method == 'GET':
        return render_template('trekker/profile.html', user=current_user)

    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        db.session.commit()
        return redirect('/trekker/dashboard')
    
@app.route('/trekker/booking/<int:booking_id>/cancel')
@login_required
def trekker_cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)

    if booking.user_id != current_user.id:
        return "Unauthorized."

    if booking.status == 'Booked':
        booking.status = 'Cancelled'
        booking.trek.available_slots += 1
        db.session.commit()

    return redirect('/trekker/bookings')