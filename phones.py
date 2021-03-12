from flask import make_response, abort
from config import db
from models import Phone, PhoneSchema


def read_all():
    """
    This function responds to a request for /api/phones
    with the complete lists of phones
    :return:        json string of list of phones
    """
    phones = Phone.query.order_by(Phone.last_name).all()
    # Serialize the data for the response
    phone_schema = PhoneSchema(many=True)
    data = phone_schema.dump(phones)
    return data


def read_one(phone_id):
    """
    This function responds to a request for /api/phones/{phone_id}
    with one matching phone from phones

    :param phone_id:   ID of phone to find
    :return:            phone matching ID
    """
    phone = Phone.query.filter(Phone.phone_id == phone_id).one_or_none()
    if phone is not None:
        # serialize the data
        phone_schema = PhoneSchema()
        return phone_schema.dump(phone).data
    else:
        abort(404, 'Phone not found for Id: {}'.format(phone_id))


def create(phone):
    """
    This function creates a new phone in the phones db
    based on the passed in phone data
    :param phone:  phone to create in phones db
    :return:        201 CREATED on success, 406 if phone exists
    """
    number = phone.get("number")

    existing_phone = Phone.query.filter(Phone.number == number).one_or_none()
    if existing_phone is None:
        schema = PhoneSchema()
        new_phone = schema.load(phone, session=db.session)
        db.session.add(new_phone)
        db.session.commit()
        return schema.dump(new_phone), 201
    else:
        abort(409, f'Phone {number} exists already')


def update(phone_id, phone):
    """
    This function updates an existing phone in the phones db
    :param phone_id:  id of the phone to update in the phones db
    :param phone:  phone to update
    :return:        updated phone db
    """
    phone_to_upd = Phone.query.filter(Phone.phone_id == phone_id).one_or_none()
    number = phone.get("number")
    existing_phone = (Phone.query.filter(Phone.number == number).one_or_none())

    if phone_to_upd is None:
        abort(404, "Phone not found for id: {}".format(phone_id))
    elif existing_phone is not None and existing_phone.phone_id != phone_id:
        abort(409, "Phone {} exists already".format(number))
    else:
        schema = PhoneSchema()
        update = schema.load(phone, session=db.session)
        update.phone_id = phone_to_upd.phone_id
        db.session.merge(update)
        db.session.commit()
        data = schema.dump(phone_to_upd)
        return data, 200


def delete(phone_id):
    """
    This function deletes a phone from the phones db
    :param phone_id:   phone number to delete
    :return:        200 on successful delete, 404 if not found
    """
    phone = Phone.query.filter(Phone.phone_id == phone_id).one_or_none()

    if phone is not None:
        db.session.delete(phone)
        db.session.commit()
        return make_response(
            "Phone {} deleted".format(phone.number), 200
        )
    else:
        abort(404, "Phone not found for Id: {}".format(phone_id))
