from sqlalchemy import UniqueConstraint
from config import db, ma
from marshmallow_sqlalchemy import ModelSchema


class Phone(db.Model):
    __tablename__ = 'phone'
    phone_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32))
    number = db.Column(db.String(32))
    __table_args__ = (UniqueConstraint('number'),)


class PhoneSchema(ModelSchema):
    class Meta:
        model = Phone
        sqla_session = db.session
