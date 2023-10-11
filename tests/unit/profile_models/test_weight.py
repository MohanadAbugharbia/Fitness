from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError


from Fitness.profile.models import Weight


# Test the Weight class
def test_empty_properties() -> None:
    weight = Weight()

    assert weight.user_id is None
    assert weight.date is None
    assert weight.weight is None


def test_properties() -> None:
    user_id = 1
    date = datetime.today()
    weight_float = 99.9

    weight = Weight(
        user_id = user_id,
        date = date,
        weight = weight_float
    )

    assert weight.user_id == user_id
    assert weight.date == date
    assert weight.weight == weight_float
    
def test_create_weight(db_session, test_user):

    user_id = test_user.id
    date = datetime(2023, 10, 11)
    weight_float = 70.5
    weight = Weight(user_id=user_id, date=date, weight=weight_float)
    db_session.add(weight)
    db_session.commit()

    saved_weights = Weight.query.filter_by(user_id=user_id, date=date).all()

    assert len(saved_weights) == 1
    saved_weight = saved_weights[0]
    assert saved_weight is not None
    assert saved_weight.user_id == user_id
    assert saved_weight.date == date
    assert saved_weight.weight == weight_float

def test_update_weight(db_session, test_user):

    user_id = test_user.id
    date = datetime(2023, 10, 12)
    weight_float = 70.5
    updated_weight_float = 75.5

    weight = Weight(user_id=user_id, date=date, weight=weight_float)
    db_session.add(weight)
    db_session.commit()

    updated_weight = Weight.query.filter_by(user_id=user_id, date=date).first()
    updated_weight.weight = updated_weight_float
    db_session.commit()

    updated_weight = Weight.query.filter_by(user_id=user_id, date=date).first()
    assert updated_weight.weight == updated_weight_float


def test_delete_weight(db_session, test_user):

    user_id = test_user.id
    date = datetime(2023, 10, 13)
    weight_float = 70.5

    weight = Weight(user_id=user_id, date=date, weight=weight_float)
    db_session.add(weight)
    db_session.commit()

    db_session.delete(weight)
    db_session.commit()

    deleted_weight = Weight.query.filter_by(user_id=user_id, date=date).first()
    assert deleted_weight is None

def test_same_user_id_same_date_weight(db_session, test_user):

    user_id = test_user.id
    date = datetime(2023, 10, 14)
    weight_float = 70.5

    weight = Weight(user_id=user_id, date=date, weight=weight_float)
    db_session.add(weight)
    db_session.commit()

    weight = Weight(user_id=user_id, date=date, weight=weight_float)
    db_session.add(weight)
    with pytest.raises(IntegrityError):
        db_session.commit()
    
  