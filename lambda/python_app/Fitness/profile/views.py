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
    weight_query = Weight.query.filter_by(user_id=user_id, date=date).first()

    if weight_query:
        flash("Date already has a weight entry!", "weight_entry_error")
        return redirect(url_for("profile.home"))

    new_weight = Weight(
        user_id = user_id,
        date = date,
        weight = weight
    )

    db.session.add(new_weight)
    db.session.commit()

    return redirect(url_for('profile.home'))