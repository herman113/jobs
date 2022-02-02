from flask_app import app # NEED this line for app.route() among other things
from flask import render_template, redirect, request, session
from flask_app.models import user # Import your models here
from flask_bcrypt import Bcrypt # NEW - for hashing passwords
from flask_app import app # Needed for bcrypt as well
bcrypt = Bcrypt(app)

"""
0. Login/registration PAGE
1. Register (POST) - Create a new user - after validating to make sure the data in the form are valid.
2. Login (POST) - Log in a user who created an account
3. Dashboard page after registering/logging in - MUST BE LOGGED IN
4. Logout - leave the site
"""

@app.route("/") # Show login/registration page
def index():
    if "user_id" in session: # If logged in, send the user to the "dashboard" landing page
        return redirect("/dashboard")
    return render_template("login_reg_page.html")

@app.route("/register", methods=["POST"])
def register_new_user():
    # Validate data
    if not user.User.validate_registration(request.form): # Form is invalid
        return redirect("/") # Send user back
    # If we reach this point, the form IS valid
    # Create the new user
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    # Save new user id in session if successful
    session["user_id"] = user.User.create_new_user(data)
    # Send to dashboard (landing) page
    return redirect("/dashboard") # To be added in next lecture

@app.route("/login", methods=["POST"])
def login_user():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    is_valid_or_id = user.User.validate_login(data)
    if is_valid_or_id == False: # Invalid input from form
        return redirect("/") # Send person back to login-registration page
    else:
        session["user_id"] = is_valid_or_id # Set session variable = ID of identified user
        return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear() # Removes all session variables
    return redirect("/")
