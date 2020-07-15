from app import app
from db import db

db.init_app(app)

# Before processing any requests tell SQLAlchemy to create the database if not
# available.
@app.before_first_request
def create_tables():
    db.create_all()
