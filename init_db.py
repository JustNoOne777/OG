from ext import app, db
from models import User

with app.app_context():

    db.drop_all()
    db.create_all()

    admin_user = User(username="Admin", password="noonecangetthis777", role="Admin" )
    admin_user.create()
    admin_user = User(username="Moderator", password="moderpass777", role="Moderator" )
    admin_user.create()