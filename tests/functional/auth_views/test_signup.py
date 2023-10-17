from flask.testing import FlaskClient
from Fitness.auth.models import User, LoginForm, SignupForm



def test_signup_page(client: FlaskClient):
    response = client.get("/signup")
    assert response.status_code == 200

def test_signup_post(client: FlaskClient):
    firstname = "testfirstname"
    lastname = "testlastname"
    password = "testpassword"
    email = "testsignuppost@example.com"
    data = {
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
        "email": email
    }
    
    response = client.post("/signup", data=data)

    user: User = User.query.filter_by(email=email).first()
    assert response.headers.get("Location") == "/login"
    assert response.status_code == 302
    assert user is not None
    assert user.firstname == firstname
    assert user.lastname == lastname
    assert user.verify_password(password) is True

def test_signup_post_invalid_email(client: FlaskClient):
    email = "XXXXXXXXXXXX"
    data = {
        "email": email
    }

    response = client.post("/signup", data=data)
    assert response.status_code == 400
    assert "invalid email" in response.data.decode("utf-8").lower()

def test_signup_post_short_password(client: FlaskClient):
    password = "hi"
    data = {
        "password": password,
    }

    response = client.post("/signup", data=data)
    assert response.status_code == 400
    assert "password must be at least" in response.data.decode("utf-8").lower()

def test_signup_post_long_password(client: FlaskClient):
    password = "X"*200
    data = {
        "password": password,
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 400
    assert "password must be less than" in response.data.decode("utf-8").lower()

def test_signup_post_64_char_password(client: FlaskClient):
    password = "X"*64
    data = {
        "password": password,
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 400
    assert "password must be less than" not in response.data.decode("utf-8").lower()
    assert "password must be at least" not in response.data.decode("utf-8").lower()