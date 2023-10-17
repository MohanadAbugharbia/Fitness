import pytest
from tools import DatabaseConfig, ApplicationConfig
from Fitness import create_app, db
from Fitness.auth.models import User


app_config = ApplicationConfig(
    secret_key="XXXXXXXX"
)
db_config = DatabaseConfig(
    user="postgres",
    password="testpassword",
    host="localhost",
    port=5432,
    database="testdb",
    engine="postgresql"
)



@pytest.fixture(scope="session")
def app():
    app = create_app(db_config, app_config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def db_session(app):
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()

@pytest.fixture(scope="module")
def test_user(db_session):
    user = User(
        email="testuser@example.com",
        firstname="test",
        lastname="user",
        password="testpassword"
    )
    db_session.add(user)
    db_session.commit()
    
    return user

@pytest.fixture(scope="module")
def test_client(app):
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client