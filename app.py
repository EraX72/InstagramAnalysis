from flask import Flask, render_template, redirect, session, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from instabot import Bot
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

def login_with_instabot(username, password):
    bot = Bot()
    try:
        bot.login(username=username, password=password)
        return True, bot
    except Exception as e:
        print(f"Login failed: {e}")
        return False, None

def fetch_media_data(bot, user_id):
    media_data = []
    try:
        for media_id in bot.get_user_medias(user_id, filtration=None):
            media = bot.get_media_info(media_id)
            media_data.append(media)
    except Exception as e:
        print(f"Error fetching media data: {e}")
    return media_data

def analyze_account(bot, target_username):
    try:
        user_id = bot.get_user_id_from_username(target_username)

        user_info = bot.get_user_info(user_id)

        print(f"Username: {user_info['username']}")
        print(f"Full Name: {user_info['full_name']}")
        print(f"Number of Posts: {user_info['media_count']}")
        print(f"Number of Followers: {user_info['follower_count']}")
        print(f"Number of Following: {user_info['following_count']}")

        followers = bot.get_user_followers(user_id)
        following = bot.get_user_following(user_id)

        mutual_followers = [follower for follower in followers if follower in following]
        unfollowed_back = [follower for follower in followers if follower not in following]
        stalked_back = [follower for follower in followers if follower not in following and follower not in mutual_followers]

        print(f"Mutual Followers:")
        for mutual_follower in mutual_followers:
            print(f" - {mutual_follower['username']}")

        print(f"Unfollowed Back:")
        for unfollowed in unfollowed_back:
            print(f" - {unfollowed['username']}")

        print(f"Stalked Back:")
        for stalked in stalked_back:
            print(f" - {stalked['username']}")

        media_data = fetch_media_data(bot, user_id)

        print(f"Media Data:")
        for media in media_data:
            print(f" - {media['id']}: {media['caption']['text']}")

        return user_info, mutual_followers, unfollowed_back, stalked_back, media_data

    except Exception as e:
        print(f"Error analyzing account: {e}")
        return None, None, None, None, None

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, bot = login_with_instabot(username, password)

        if success:
            user = User()
            user.id = bot.user_id
            login_user(user)

            flash('Login successful!', 'success')
            return redirect(url_for('analysis'))

        flash('Login failed. Please check your credentials.', 'error')

    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
@login_required
def analysis():
    bot = Bot()
    bot.user_id = current_user.id

    user_info, mutual_followers, unfollowed_back, stalked_back, media_data = analyze_account(bot, current_user.id)

    return render_template('analysis.html', user_info=user_info, mutual_followers=mutual_followers,
                           unfollowed_back=unfollowed_back, stalked_back=stalked_back, media_data=media_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)