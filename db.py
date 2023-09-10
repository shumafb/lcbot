import sqlalchemy as db
import bot

engine = db.create_engine('sqlite:///db///db.sqlite')

conn = engine.connect()

metadata = db.MetaData()

users = db.Table('users', metadata,
                 db.Column('user_id', db.Integer, primary_key=True),
                 db.Column('pass_check', db.Boolean, default=False)
)


# def add_user(user_id, pass_check):
#     add_query = users.insert().values({'user_id': user_id, 'pass_check': pass_check})
#     conn.execute(add_query)


select_all = db.select([users])

select_all_results = conn.execute(select_all)

print(select_all_results.fetchall())