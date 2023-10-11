import pytest
from sqlalchemy.exc import IntegrityError


from Fitness.auth.models import User


def test_personal_properties():
    email = "testemail@test.com"
    firstname = "TestFirstName"
    lastname = "TestLastName"
    password = "TestPasword"

    user = User(
        email = email,
        firstname = firstname,
        lastname = lastname,
        password = password
    )
    assert user.email == email
    assert user.firstname == firstname
    assert user.lastname == lastname

def test_empty_properties():
    user = User()
    assert user.email is None
    assert user.firstname is None
    assert user.lastname is None
    assert user.password_hash is None

def test_password_hash():
    password = "XXXXXXXXXXXX"
    user = User(password = password)
    assert user.password_hash is not None
    assert user.password_hash != password
    assert user.verify_password(password) is True
    assert user.verify_password("YYYYYYYYYYYY") is False
    assert user.verify_password("") is False

# test the read only property of the password attribute
def test_password_read_only():
    password = "XXXXXXXXXXXX"
    user = User(password = password)
    with pytest.raises(AttributeError):
        _ = user.password

def test_update_password(db_session):
    email="testupdatepassword@example.com"
    firstname="update"
    lastname="password"
    old_password = "XXXXXXXXXXXX"
    new_password = "YYYYYYYYYYYY"

    user = User(
        email = email,
        firstname = firstname,
        lastname = lastname,
        password = old_password
    )
    
    db_session.add(user)
    db_session.commit()

    assert user.verify_password(old_password) is True
    assert user.verify_password(new_password) is False

    user.password = new_password
    db_session.add(user)
    db_session.commit()

    new_user = User.query.filter(email == email).first()
    assert new_user.verify_password(new_password) is True
    assert new_user.verify_password(old_password) is False

def test_same_email_user(db_session):
    email="testsameemailuser@example.com"
    firstname="update"
    lastname="password"
    password = "XXXXXXXXXXXX"

    user = User(
        email = email,
        firstname = firstname,
        lastname = lastname,
        password = password
    )
    
    db_session.add(user)
    db_session.commit()

    user2 = User(
        email = email,
        firstname = firstname,
        lastname = lastname,
        password = password
    )

    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()