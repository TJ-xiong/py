from datetime import datetime

from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    articles = db.relationship('Article', back_populates='author')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            # ⚠️ 密码一般不返回
        }
