from flask import flash
import instaloader
from flask_login import UserMixin

class User(UserMixin):
    pass

def login(username, password, access_token):
    if username and password:
        try:
            api = instaloader.Instaloader()
            api.context = instaloader.InstaloaderContext()
            api.context.log_in(username, password)
            user_id = api.context.logged_in_user_id
            user_token = api.context.logged_in_user_token

            flash(f"Login successful. User ID: {user_id}", 'success')
            return api, user_id, user_token
        except Exception as e:
            flash(f"Login failed: {e}", 'error')
            return None, None, None
    elif access_token:
        # Perform login using access token
        pass
    else:
        flash("Invalid login details.", 'error')
        return None, None, None