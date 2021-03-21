from app import db
from app.models import User, generate_password_hash

user = User.query.first()
pwd = input ('Type new password for user %s: ' % user.username)
user.password_hash=generate_password_hash(pwd)
db.session.commit()


