import sqlalchemy as db
import bot

engine = db.create_engine('sqlite:///source///db.sqlite')

conn = engine.connect()

metadata = db.MetaData()

users = db.Table('users', metadata,
                 db.Column('user_id', db.Integer, primary_key=True),
                 db.Column('pass_check', db.Boolean, default=False)
)


def add_user(user_id, pass_check):
    add_query = users.insert().values({'user_id': user_id, 'pass_check': pass_check})
    conn.execute(add_query)