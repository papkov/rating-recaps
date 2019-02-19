from flask import Flask
from config import Config


app = Flask(__name__)
# SESSION_TYPE = 'redis'

app.jinja_env.globals.update(zip=zip)
app.config.from_object(Config)


from app import routes
