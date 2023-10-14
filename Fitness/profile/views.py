from logging import getLogger
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import desc
from Fitness.profile.models import (
    WeightForm,
    Weight,
)
from Fitness import db

profile = Blueprint('profile', __name__)
logger = getLogger("Fitness")

@profile.route("/profile")
@login_required
def home():
    weight_form=WeightForm(request.form)
    weights = Weight.query.filter_by(user_id = current_user.id).order_by(desc(Weight.date)).all()
    return render_template("profile.html", user=current_user, weight_form=weight_form, weights=weights)

@profile.route("/profile/submit_weight", methods=["POST"])
@login_required
def submit_weight():
    form: WeightForm = WeightForm(request.form)
    if form.errors:
        flash(form.errors, "weight_entry_error")
        redirect(url_for('profile.home'))

    date = request.form.get("date")
    weight = request.form.get("weight")
    user_id = current_user.id
    weight_obj = Weight.query.filter_by(user_id=user_id, date=date).first()

    if not weight_obj:
        weight_obj = Weight(user_id=user_id, date=date)

    weight_obj.weight = weight

    logger.debug(f"user id '{weight_obj.user_id}' submitted weight '{weight_obj.weight}' for {weight_obj.date}")

    db.session.add(weight_obj)
    db.session.commit()

    return redirect(url_for('profile.home'))