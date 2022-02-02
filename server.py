from flask_app import app
from flask_app.controllers import users, jobs # IMPORTANT - IMPORT ALL YOUR CONTROLLER FILES HERE!

if __name__ == "__main__":
    app.run(debug=True)