from web.database import db
from web.models import (
    Player, Game, Round, Hint,
)

# Re-create all tables
db.drop_all()
db.create_all()

game = Game(id='hackvan', title='Hackvan Trivia', description='This is the hackvan game',
    rounds=[
        Round(round_number=0, answer='lego', hints=[
            Hint(position=2, hint="I have my own theme park in Denmark. Over 200 billion of me have been produced"),
            Hint(position=0, hint="I was invented in 1949 By Ole Christianson"),
            Hint(position=1, hint="I'm made of molded plastic and come in 1700 shapes and every color"),
        ]),
        Round(round_number=1, answer='everest', hints=[
            Hint(position=2, hint="It is a landmark in Nepal"),
            Hint(position=0, hint="It is known as Chomolungma in its native language"),
            Hint(position=1, hint="It is the purpose of life for Edmund Hillary"),
        ]),
        Round(round_number=2, answer='toes', hints=[
            Hint(position=2, hint="They hide in your shoes and you have 10 of them"),
            Hint(position=0, hint="They come in different sizes"),
            Hint(position=1, hint="They are with you since you are born and help you walk"),
        ]),        
    ],
)

db.session.add_all([
    game
])
db.session.commit()


