from .models import db, User, StaffProfile, Trek, Booking
from flask import current_app as app
from datetime import date

with app.app_context():
    db.create_all()

    if User.query.filter_by(role='admin').first() is None:
        admin = User(
            name='Admin',
            email='admin@trek.com',
            password='admin123',
            role='admin',
            phone='9999999999',
            status='active'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created.")

    if User.query.filter_by(role='staff').first() is None:
        staff1_user = User(
            name='Ishan Jindal',
            email='ishan@gmail.com',
            password='staff123',
            role='staff',
            phone='8888888881',
            status='active'
        )
        staff2_user = User(
            name='Priya Sharma',
            email='priya@gmail.com',
            password='staff123',
            role='staff',
            phone='8888888882',
            status='active'
        )
        db.session.add(staff1_user)
        db.session.add(staff2_user)
        db.session.commit()

        staff1_profile = StaffProfile(
            user_id=staff1_user.id,
            bio='Experienced mountaineer with 8 years in the Himalayas.',
            exp_years=8,
            status='approved'
        )
        staff2_profile = StaffProfile(
            user_id=staff2_user.id,
            bio='Certified trekking guide specializing in Western Ghats.',
            exp_years=5,
            status='approved'
        )
        db.session.add(staff1_profile)
        db.session.add(staff2_profile)
        db.session.commit()
        print("Staff created.")

    if User.query.filter_by(role='trekker').first() is None:
        trekker1 = User(
            name='Shagun Chadha',
            email='shagun@gmail.com',
            password='trekker123',
            role='trekker',
            phone='7777777771',
            address='Sector-15 Rohini,New Delhi',
            status='active'
        )
        trekker2 = User(
            name='Bharti Bhatti',
            email='bharti@gmail.com',
            password='trekker123',
            role='trekker',
            phone='7777777772',
            address='Moti Bagh, South Delhi',
            status='active'
        )
        db.session.add(trekker1)
        db.session.add(trekker2)
        db.session.commit()
        print("Trekkers created.")

    if Trek.query.first() is None:
        staff1_profile = StaffProfile.query.first()
        staff2_profile = StaffProfile.query.all()[1] if len(StaffProfile.query.all()) > 1 else None

        trek1 = Trek(
            name='Valley of Flowers',
            location='Uttarakhand',
            difficulty='Moderate',
            duration=6,
            total_slots=20,
            available_slots=20,
            status='Open',
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 7),
            description='A beautiful trek through alpine meadows.',
            assigned_staff_id=staff1_profile.id if staff1_profile else None
        )
        trek2 = Trek(
            name='Roopkund Trek',
            location='Chamoli, Uttarakhand',
            difficulty='Hard',
            duration=8,
            total_slots=15,
            available_slots=15,
            status='Open',
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 18),
            description='High altitude trek to the mysterious skeleton lake.',
            assigned_staff_id=staff2_profile.id if staff2_profile else None
        )
        trek3 = Trek(
            name='Coorg Tadiyandamol',
            location='Coorg, Karnataka',
            difficulty='Easy',
            duration=2,
            total_slots=30,
            available_slots=30,
            status='Open',
            start_date=date(2025, 8, 5),
            end_date=date(2025, 8, 7),
            description='A refreshing easy trek through coffee plantations.',
            assigned_staff_id=None
        )
        db.session.add(trek1)
        db.session.add(trek2)
        db.session.add(trek3)
        db.session.commit()
        print("Treks created.")