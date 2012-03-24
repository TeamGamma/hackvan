from web.database import db
from web.models import (
    Player, Game, Round, Hint,
)

# Re-create all tables
db.drop_all()
db.create_all()

player = Player(phone='6048916649', points=0)
game = Game(id='game_zero', title='Game Zero', description='The first game',
    rounds=[
        Round(round_number=0, answer='Lego', hints=[
            Hint(position=2, hint="Initially only in red and white, but green blue and yellow came shortly after"),
            Hint(position=0, hint="Invented in 1949 By Ole Christianson"),
            Hint(position=1, hint="My company slogan is  'the best is never too good'"),
        ]),
    ],
    players=[player],
)

db.session.add_all([
    player
])
db.session.commit()


