from .models import db, User, StaffProfile, Trek, Booking, Review
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
            description='A beautiful trek through alpine meadows with wildflowers and glacial streams.',
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
            description='High altitude trek to the mysterious skeleton lake with striking alpine views.',
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
            description='A refreshing easy trek through coffee plantations and misty ridges.',
            assigned_staff_id=None
        )
        trek4 = Trek(
            name='Hampta Pass',
            location='Himachal Pradesh',
            difficulty='Hard',
            duration=5,
            total_slots=12,
            available_slots=12,
            status='Open',
            start_date=date(2025, 9, 12),
            end_date=date(2025, 9, 17),
            description='A dramatic pass crossing through green valleys and glacial terrain.',
            assigned_staff_id=staff1_profile.id if staff1_profile else None
        )
        db.session.add(trek1)
        db.session.add(trek2)
        db.session.add(trek3)
        db.session.add(trek4)
        db.session.commit()

        trekkers = User.query.filter_by(role='trekker').all()

        if Review.query.first() is None:
            sample_reviews = [
                Review(user_id=trekkers[0].id, trek_id=trek1.id, rating=5, comment='The scenery was breathtaking and the guide was excellent.'),
                Review(user_id=trekkers[1].id, trek_id=trek2.id, rating=4, comment='Challenging but incredibly rewarding.'),
                Review(user_id=trekkers[0].id, trek_id=trek3.id, rating=5, comment='Perfect weekend escape with lovely views.'),
            ]
            db.session.add_all(sample_reviews)
            db.session.commit()

        if Booking.query.first() is None:
            sample_bookings = [
                Booking(user_id=trekkers[0].id, trek_id=trek1.id, status='Booked', payment_status='Paid'),
                Booking(user_id=trekkers[1].id, trek_id=trek2.id, status='Booked', payment_status='Paid'),
                Booking(user_id=trekkers[0].id, trek_id=trek4.id, status='Booked', payment_status='Pending'),
            ]
            db.session.add_all(sample_bookings)
            db.session.commit()
        print("Treks created.")