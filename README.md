Trekking Management Application

This is a Flask-based web application for managing trekking activities, bookings, staff assignments, and trekker reviews. The system supports three roles:
- Admin
- Trek Staff
- Trekkers

Project Overview
Adventure organizations often rely on spreadsheets and manual coordination to manage trekking activities. This application provides a centralized platform to manage treks, bookings, staff approval, and trekker feedback.

Features
- User registration and login
- Role-based access for admin, staff, and trekkers
- Admin management of treks, staff, users, and bookings
- Staff management of assigned treks and participants
- Trekker browsing, booking, and trek review functionality
- Responsive UI built with Bootstrap

Requirements
Make sure Python is installed on your system.

Setup Instructions
1. Open the project folder in your terminal.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and go to:
   ```text
   http://127.0.0.1:5000/
   ```

Default Login Credentials
- Admin:
  - Email: admin@trek.com
  - Password: admin123
- Staff:
  - Email: priya@gmail.com
  - Password: staff123
- Trekker:
  - Email: shagun@gmail.com
  - Password: trekker123

Project Structure
- app.py - Main Flask application entry point
- backend/models.py - Database models
- backend/routes.py - Application routes and logic
- templates/ - HTML templates for the application UI
- instance/ - SQLite database file

Notes
- The app uses SQLite by default.
- On first run, initial sample data will be created automatically.
- If you want to reset the database, delete the file in the instance folder and run the app again.