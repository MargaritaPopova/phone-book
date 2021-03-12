from flask import make_response, abort


PHONES = {
    "87656448839": {
        "first_name": "Doug",
        "last_name": "Farrell",
        "number": '87656448839'
    },
    "84767658907": {
        "first_name": "Kent",
        "last_name": "Brockman",
        "number": '84767658907'
    },
    "84563289754": {
        "first_name": "Bunny",
        "last_name": "Easter",
        "number": '84563289754'
    }
}


def read_all():
    """
    This function responds to a request for /api/phones
    with the complete lists of phones
    :return:        json string of list of phones
    """
    return [PHONES[key] for key in sorted(PHONES.keys())]


def read_one(number):
    """
    This function responds to a request for /api/phones/{pk}
    with one matching phone from phones
    :param number:   pk of phone to find
    :return:        phone matching pk
    """
    phone = {}
    if number in PHONES:
        phone = PHONES.get(number)
    else:
        abort(404, "phone with number {number} not found".format(number=number))
    return phone


def create(phone):
    """
    This function creates a new phone in the phones structure
    based on the passed in phone data
    :param phone:  phone to create in phones structure
    :return:        201 on success, 406 if phone exists
    """
    first_name = phone.get("first_name", None)
    last_name = phone.get("last_name", None)
    number = phone.get("number", None)

    if number not in PHONES and number is not None:
        PHONES[number] = {
            "first_name": first_name,
            "last_name": last_name,
            "number": number,
        }
        return make_response(
            "{number} successfully created".format(number=number), 201
        )
    else:
        abort(406, "phone with number {number} already exists".format(number=number))


def update(number, phone):
    """
    This function updates an existing phone in the phones structure
    :param number:  phone number to update in the phones structure
    :param phone:  phone to update
    :return:        updated phone structure
    """
    if number in PHONES:
        PHONES[number]["first_name"] = phone.get("first_name")
        PHONES[number]["last_name"] = phone.get("last_name")
        PHONES[number]["number"] = number
        return PHONES[number]
    else:
        abort(404, "phone with last number {number} not found".format(number=number))


def delete(number):
    """
    This function deletes a phone from the phones structure
    :param number:   phone number to delete
    :return:        200 on successful delete, 404 if not found
    """
    if number in PHONES:
        del PHONES[number]
        return make_response(
            "{number} successfully deleted".format(number=number), 200
        )
    else:
        abort(404, "phone with number {number} not found".format(number=number))
