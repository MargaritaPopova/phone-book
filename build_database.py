import os
from config import db
from models import Phone

# Data to initialize database with
PHONES = [
    {"first_name": "Doug", "last_name": "Farrell", "number": "32497238473"},
    {"first_name": "Lesley", "last_name": "Doe", "number": "87867675655"},
    {"first_name": "Minnie", "last_name": "Marshall", "number": "97654333567"},
    {"first_name": "John", "last_name": "Link", "number": "76353344333"},
]

# Delete database file if it exists currently
if os.path.exists("phones.db"):
    os.remove("phones.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for phone in PHONES:
    p = Phone(
        first_name=phone.get("first_name"),
        last_name=phone.get("last_name"),
        number=phone.get("number")
    )
    db.session.add(p)

db.session.commit()
