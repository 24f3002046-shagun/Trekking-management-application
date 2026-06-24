from flask import current_app as app

@app.route('/')
def home():
    return("This is trekking management app")