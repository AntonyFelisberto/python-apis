import os
import uuid
import requests
from db import db
from models import UserModel
from schemas import UserSchema,UserRegisterSchema
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint, abort
from blocklist import BLOCKLIST
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import create_access_token,jwt_required,get_jwt, create_refresh_token, get_jwt_identity

blp = Blueprint("Users","users",description="Operations on users")

def send_simple_message(to,subject,body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api",os.getenv("MAILGUN_API_KEY")),
        data={
            "from":"YOUR MAIL FROM THE MAILGUN",
            "to":[to],
            "subject":subject,
            "text":body
        }
    )

@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
                )
            ).first():
            abort(409,message="user or email already exists")

        user = UserModel(
            username=user_data["username"],
            email = user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        try:
            send_simple_message(
                to=user.email,
                subject="sucessfully signed up",
                body="hi you has been registered"
            )
        except:
            print("didn't send the e-mail")

        return {"message": "user created sucessfully"}, 201

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token":new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token":access_token,"refresh_token":refresh_token}
        
        abort(401,message="Invalid Credentials")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.arguments(UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted sucessfully"}, 200