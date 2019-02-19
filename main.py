from app import app
from flask import session

if __name__ == "__main__":
    app.jinja_env.globals.update(zip=zip)
    app.run(debug=True)