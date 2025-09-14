import json
import time

from flask import Flask
from flask_migrate import Migrate

from exts import db
from model.Article import Article
from model.User import User
import config
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)


if __name__ == '__main__':
    app.run()
