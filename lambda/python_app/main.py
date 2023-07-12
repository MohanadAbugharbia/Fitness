import os
import json
import boto3
import botocore.exceptions
from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template
)
import datetime
import awsgi
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger
import requests

app = Flask(__name__)

COGNITO_LOGIN_ENDPOINT = os.environ['COGNITO_LOGIN_ENDPOINT']
FITNESS_APP_ENDPOINT = os.environ['FITNESS_APP_ENDPOINT']
FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']
COGNITO_USER_POOL_CLIENT_ID = os.environ['COGNITO_USER_POOL_CLIENT_ID']

def get_cognito_token(code: str, redirect_uri: str) -> requests.Response:
    url: str = f"https://{COGNITO_LOGIN_ENDPOINT}/oauth2/token"
    client_id: str = COGNITO_USER_POOL_CLIENT_ID
    headers: dict = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    params: dict = {
        "grant_type": 'authorization_code',
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri
    }
    response: requests.Response = requests.post(url=url, params=params, headers=headers)
    return response

def get_cognito_user(accesstoken: str) -> dict:

    client = boto3.client('cognito-idp')
    try:
        response: dict = client.get_user(
            AccessToken=accesstoken
        )
        print(response)
    except botocore.exceptions.ClientError as e:
        print(e)
        print(e.response["Error"]["Code"])
        if e.response["Error"]["Code"] in [
            "ForbiddenException",
            "InternalErrorException",
            "InvalidParameterException",
            "NotAuthorizedException",
            "PasswordResetRequiredException",
            "ResourceNotFoundException",
            "TooManyRequestsException",
            "UserNotConfirmedException",
            "UserNotFoundException"
        ]:
            logger.error(f'{e.response["Error"]["Code"]} : {e.response["Error"]["Message"]}')
        session.pop("access_token")
        return redirect(url_for('login'))

    user_info: dict = {}
    for attribute in response.get('UserAttributes'):
        user_info[attribute['Name']] = attribute['Value']

    user_info['username'] = f"{user_info['given_name']} {user_info['family_name']}"

    return user_info

@app.route('/postweight')
def post_weight():
    if not 'access_token' in session:
        return redirect(url_for('login'))
    else:
        user_info: dict = get_cognito_user(session['access_token'])
        user: str = user_info.get('username')
        return render_template("post_weight.html", user=user)


@app.route('/getweights')
def get_weights():
    if not 'access_token' in session:
        return redirect(url_for('login'))
    else:
        user_info: dict = get_cognito_user(session['access_token'])
        user: str = user_info.get('username')
        return render_template("get_weights.html", user=user)

@app.route('/login')
def login():
    if 'access_token' in session:
        return redirect(url_for('home'))
    elif not 'code' in request.args:
        client_id: str = COGNITO_USER_POOL_CLIENT_ID
        response_type: str = "code"
        cognito_endpoint: str = COGNITO_LOGIN_ENDPOINT
        scope: str = "aws.cognito.signin.user.admin+email+openid+phone+profile"
        redirect_uri: str = f"https%3A%2F%2F{FITNESS_APP_ENDPOINT}%2Flogin"

        return redirect(
            f"https://{cognito_endpoint}/login?client_id={client_id}&response_type={response_type}&scope={scope}&redirect_uri={redirect_uri}"
        )
    else:
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=60)
        session.modified = True
        code: str = request.args.get('code')
        response = get_cognito_token(code=code, redirect_uri=f"https://{FITNESS_APP_ENDPOINT}/login")
        token_info: dict = json.loads(response.text)
        if 'error' in token_info:
            return f"An error occured '{token_info.get('error')}'"
        else:
            # session['id_token'] = token_info.get('id_token')
            session['access_token'] = token_info.get('access_token')
            # session['refresh_token'] = token_info.get('refresh_token')
            session['token_type'] = token_info.get('token_type')
            session['expires_in'] = token_info.get('expires_in')
            return redirect(url_for('home'))

@app.route('/home')
def home():
    if not 'access_token' in session:
        return redirect(url_for('login'))
    else:
        user_info: dict = get_cognito_user(session['access_token'])
        user: str = user_info.get('username')
        return render_template("home.html", user=user)

@app.route('/')
def index():
    return render_template("index.html")

logger: Logger = Logger(service="FitnessApp")



@logger.inject_lambda_context()
def handler(event: dict, context: LambdaContext) -> dict:
    logger.set_correlation_id(context.aws_request_id)
    app.secret_key = FLASK_SECRET_KEY
    return awsgi.response(app=app, event=event, context=context)




if __name__=="__main__":
    class FakeLambdaContext(LambdaContext):
        aws_request_id: str = "fake aws_request_id"
        _function_name: str = "Fake function"
        def __init__(self) -> None:
            pass

    with open("test_data2.json", "r") as f:
        TEST_DATA = json.load(f)
    # handler_response: dict = handler(TEST_DATA, FakeLambdaContext())
    # print(json.dumps(handler_response, indent=4))

    response = awsgi.response(app, TEST_DATA, FakeLambdaContext())

    print(response)
    print(response['body'])

    