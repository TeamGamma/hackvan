from web.database import db
from web.utils import ReprMixin, InitMixin

class Game(InitMixin, ReprMixin, db.Model):
    id = db.Column(db.String(140), primary_key=True, nullable=False)
    title = db.Column(db.String(140), primary_key=True, nullable=False)
    description = db.Column(db.Text(), nullable=False, default="")

    # This is the index of the round in the rounds array
    current_round = db.Column(db.Integer, nullable=False, default=0)

    players = db.relationship('User', backref='game')
    rounds = db.relationship('Round', backref='game', order_by="Round.round_number")


class User(InitMixin, ReprMixin, db.Model):
    phone = db.Column(db.String(140), primary_key=True, nullable=False)
    game_id = db.Column(db.String(140), db.ForeignKey(Game.id))
    points = db.Column(db.Integer, nullable=False, default=0)


class Round(InitMixin, ReprMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_number = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.String(140), db.ForeignKey(Game.id))
    answer = db.Column(db.String(140), nullable=False)

    hints = db.relationship('Hint', backref='round', order_by="Hint.position")


class Hint(InitMixin, ReprMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_id = db.Column(db.Integer, db.ForeignKey(Round.id))
    hint = db.Column(db.String(140), nullable=False)
    position = db.Column(db.Integer, nullable=False)

