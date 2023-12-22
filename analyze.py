# analyze.py
from instagram_private_api import Client, ClientCompatPatch, ClientError

def fetch_media_data(api, user_id):
    media_data = []
    try:
        for media in api.user_media_feed(user_id):
            media_data.append(media)
    except ClientError as e:
        print(f"Error fetching media data: {e}")
    return media_data

def analyze_account(api, username):
    try:
        # Get the user ID for the specified username
        user_id = api.user_id_from_username(username)

        # Fetch user data, including followers and following
        user_info = api.user_info(user_id)

        # Print user data
        print(f"Username: {user_info['username']}")
        print(f"Full Name: {user_info['full_name']}")
        print(f"Number of Posts: {user_info['media_count']}")
        print(f"Number of Followers: {user_info['follower_count']}")
        print(f"Number of Following: {user_info['following_count']}")

        # Get a list of followers
        followers = api.user_followers(user_id)

        # Get a list of following
        following = api.user_following(user_id)

        # Get a list of mutual followers, unfollowed back, and stalked back
        mutual_followers = [follower for follower in followers if follower in following]
        unfollowed_back = [follower for follower in followers if follower not in following]
        stalked_back = [follower for follower in followers if follower not in following and follower not in mutual_followers]

        # Print mutual followers, unfollowed back, and stalked back
        print(f"Mutual Followers:")
        for mutual_follower in mutual_followers:
            print(f" - {mutual_follower['username']}")

        print(f"Unfollowed Back:")
        for unfollowed in unfollowed_back:
            print(f" - {unfollowed['username']}")

        print(f"Stalked Back:")
        for stalked in stalked_back:
            print(f" - {stalked['username']}")

        # Fetch media data for the user
        media_data = fetch_media_data(api, user_id)

        # Print media data
        print(f"Media Data:")
        for media in media_data:
            print(f" - {media['id']}: {media['caption']}")

    except Exception as e:
        print(f"Error analyzing account: {e}")

# Your Instagram API keys and access tokens
user_name = 'YOUR_USER_NAME'
password = 'YOUR_PASSWORD'

# Initialize the Instagram API object
api = Client(user_name, password)
ClientCompatPatch(api)

# Call the analyze_account function with the API object and the target username
analyze_account(api, 'target_username')
