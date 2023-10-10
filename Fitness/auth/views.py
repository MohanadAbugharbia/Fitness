from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    Blueprint,
    g,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)
from Fitness import login_manager,db
from Fitness.auth.models import (
    User,
    LoginForm,
    SignupForm
)


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.before_request
def get_current_user():
    g.user = current_user

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', "info")
        return redirect(url_for('home'))
    form = LoginForm(request.form)
 
    return render_template('login.html', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    print(request.args)
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user: User = User.query.filter_by(email=email).first()
    if user is None or user.verify_password(password) is False:
        flash('Please check your login details and try again', 'error')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    flash("Successfully logged in", "info")
    return redirect(url_for('home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@auth.route("/signup")
def signup():
    if current_user.is_authenticated:
        flash('You are already logged in.', "info")
        return redirect(request.referrer) if request.referrer else redirect(url_for('home'))
    form = SignupForm(request.form)
    return render_template("signup.html", form=form)


@auth.route("/signup", methods=["POST"])
def signup_post():
    form = SignupForm(request.form)
    if form.errors:
        flash(form.errors, 'error')
        return redirect(url_for("auth.signup"))
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')

    user: User = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists', 'error')
        return redirect(url_for("auth.signup"))

    new_user = User(
        email = email,
        firstname = firstname,
        lastname = lastname,
        password = password,
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))