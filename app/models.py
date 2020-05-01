from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    friends = db.relationship('Friend', backref='user', lazy=True)

    def register_friends(self, friends):
        for friend in friends:
            friend_model = Friend(
                first_name=friend['first_name'],
                last_name=friend['last_name'],
                city=('No information' if friend.get('city') is None else friend['city']['title']),
                user_id=self.id
            )
            friend_model.commit_to_db()

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
