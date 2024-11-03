from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import base64
import asyncio
import aiohttp  

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

async def unfollow_user(session, username, headers):
    """
    Asynchronously unfollows a single GitHub user.

    Parameters:
        session (aiohttp.ClientSession): The aiohttp session for making requests.
        username (str): GitHub username to unfollow.
        headers (dict): Authorization headers for the GitHub API.

    Returns:
        str: Result message about the unfollow action.
    """
    url = f"https://api.github.com/user/following/{username}"
    async with session.delete(url, headers=headers) as response:
        if response.status == 204:
            return f"Unfollowed {username}."
        elif response.status == 404:
            return f"{username} not found or already unfollowed."
        else:
            return f"Seems Invalid Key"

async def unfollow_users_async(usernames, access_token):
    """
    Asynchronously unfollows a list of GitHub users concurrently.

    Parameters:
        usernames (list): List of GitHub usernames to unfollow.
        access_token (str): GitHub Personal Access Token with user scope.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with aiohttp.ClientSession() as session:
        tasks = [unfollow_user(session, username, headers) for username in usernames]
        results = await asyncio.gather(*tasks)
        
    for result in results:
        if result == "Seems Invalid Key":
            break
        print(result)


def get_github_followers_and_following(github_username, github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Initialize empty lists for followers and following
    followers = []
    following = []

    # Function to get paginated results
    def get_paginated_results(url):
        all_items = []
        page = 1
        
        while True:
            response = requests.get(url, headers=headers, params={'page': page, 'per_page': 100})  # Change per_page to 100 for more results
            if response.status_code == 200:
                data = response.json()
                if not data:  # Break the loop if no more data
                    break
                all_items.extend(data)
                page += 1
            else:
                if page == 1:
                    # Key has error
                    return -1
                print(f"Failed to retrieve data: {response.status_code}, {response.json()}")
                break

        return all_items

    # Get followers
    followers_url = f'https://api.github.com/users/{github_username}/followers'
    followers = get_paginated_results(followers_url)
    if isinstance(followers, int):
       return None,None,False

    followers_usernames = [follower['login'] for follower in followers]

    # Get following
    following_url = f'https://api.github.com/users/{github_username}/following'
    following = get_paginated_results(following_url)
    following_usernames = [following_user['login'] for following_user in following]

    return followers_usernames, following_usernames, True




def unfollow_users(usernames, access_token):
    """
    Wrapper to run the asynchronous unfollow function synchronously.

    Parameters:
        usernames (list): List of GitHub usernames to unfollow.
        access_token (str): GitHub Personal Access Token with user scope.
    """
    asyncio.run(unfollow_users_async(usernames, access_token))

def check_github_repo(username):
    try:
        github_url = 'https://github.com/' + username
        response = requests.get(github_url)
        return response.status_code == 200
    except Exception as e:
        return False

def scrape_github_data(base_url, end_message, username, tab):
    page = 1
    concatenated_html = ""
    
    while True:
        url = f"{base_url}?page={page}&tab={tab}"
        response = requests.get(url)
        html = response.text
        concatenated_html += html
        
        soup = BeautifulSoup(html, 'html.parser')
        if end_message in soup.text:
            break
        
        page += 1
    
    return concatenated_html

def extract_usernames_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    usernames = []
    for user_tag in soup.find_all('a', class_='d-inline-block no-underline mb-1'):
        username = user_tag.get('href')
        if username:
            usernames.append(f"@{username.split('/')[-1]}")
    return usernames

def scrape_followings(username):
    base_url = f"https://github.com/{username}"
    end_message = "That’s it. You’ve"
    return scrape_github_data(base_url, end_message, username, "following")

def scrape_followers(username):
    base_url = f"https://github.com/{username}"
    end_message = "That’s it. You’ve"
    return scrape_github_data(base_url, end_message, username, "followers")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/github', methods=['POST', 'OPTIONS'])
def give_datas():
    data = request.get_json()

    if not data or 'username' not in data or 'key' not in data or 'unfollow_not_followback' not in data or 'unfollow_all_users' not in data:
        return jsonify({'status': 'failed',"error":"15"}), 200

    username = data['username']
    encoded_key = data['key']
    check_followback = data['unfollow_not_followback']
    check_all = data['unfollow_all_users']

    try:
        decoded_key = base64.b64decode(encoded_key).decode('utf-8')
    except Exception as e:
        return jsonify({"error": "13", "status": "failed"}), 200

    isExisting = check_github_repo(username)
    if not isExisting:
        return jsonify({'status': 'failed',"error":"14"})

    if decoded_key != "Empty":
        # Get followers and following
        followers, following,isGood = get_github_followers_and_following(username, decoded_key)
        if isGood == False:
            return jsonify({"error": "12", "status": "failed"}), 200

        following_names = list(dict.fromkeys(following))
        followers_names = list(dict.fromkeys(followers))

        not_following_back = [user for user in following_names if user not in followers_names]

        print("Key Found!, Unfollowing users RN")
        if check_all == True or check_followback == True:
            if check_all == True:
                unfollow_users(following_names, decoded_key)
            if check_followback == True:
                unfollow_users(not_following_back,decoded_key)

            # Get the the Updated Infos
            followers,following,isGood =get_github_followers_and_following(username, decoded_key);
            if isGood == False:
                return jsonify({"error": "12", "status": "failed","details":"second step failed"}), 200
            following_names = list(dict.fromkeys(following))
            followers_names = list(dict.fromkeys(followers))

            not_following_back = [user for user in following_names if user not in followers_names]


    else:
        following_html = scrape_followings(username)
        followers_html = scrape_followers(username)

        following_names = extract_usernames_from_html(following_html)
        followers_names = extract_usernames_from_html(followers_html)

        following_names = list(dict.fromkeys(following_names))
        followers_names = list(dict.fromkeys(followers_names))

        not_following_back = [user for user in following_names if user not in followers_names]


    not_followed_by_me = [user for user in followers_names if user not in following_names]

    response_data = {
        'status': 'success',
        'followers_count': len(followers_names),
        'following_count': len(following_names),
        'not_following_back': not_following_back,
        'not_followed_by_me': not_followed_by_me
    }

    return jsonify(response_data)

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

if __name__ == '__main__':
    app.run(debug=True)

