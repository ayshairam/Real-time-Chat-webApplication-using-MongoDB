import bcrypt
from db import users_col


def signup_user(username, email, password):
    if users_col.find_one({"email": email}):
        return False, "Email already registered."

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_col.insert_one({
        "username": username,
        "email": email,
        "password": hashed_pw
    })
    return True, "Signup successful."


def login_user(email, password):
    user = users_col.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return True, user
    return False, None
