import secrets
from secrets import token_urlsafe

SECRET_KEY = secrets.token_urlsafe(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'