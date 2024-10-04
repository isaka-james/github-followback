from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

import requests

def check_github_repo(username):
    try:
        github_url = 'https://github.com/'+username
        # Send a request to the GitHub URL
        response = requests.get(github_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            return True
        else:
            # If the status code is not 200, check the title for "Page not found"
            if "Page not found · GitHub" in response.text:
                return False
            else:
                return False
                
    except Exception as e:
        #print(f"An error occurred: {e}")
        return False

# Function to scrape GitHub data (followings or followers)
def scrape_github_data(base_url, end_message, username, tab):
    page = 1
    concatenated_html = ""
    
    while True:
        # Build the URL with the current page number in the correct position
        url = f"{base_url}?page={page}&tab={tab}"
        
        # Print the current page being scraped
        print(f"Scraping {url}...")
        
        # Send a request to fetch the HTML content
        response = requests.get(url)
        html = response.text
        
        # Add the HTML content to the concatenated variable
        concatenated_html += html
        
        # Check if the end message is in the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        if end_message in soup.text:
            print(f"End message found on page {page}.")
            break  # Stop scraping when the end message is found
        
        # Increment the page number for the next iteration
        page += 1
    
    return concatenated_html

# Function to extract usernames from the concatenated HTML
def extract_usernames_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    usernames = []
    
    # Find all the anchor tags with a username
    for user_tag in soup.find_all('a', class_='d-inline-block no-underline mb-1'):
        username = user_tag.get('href')
        if username:
            # Add username starting with '@'
            usernames.append(f"@{username.split('/')[-1]}")
    
    return usernames

# Function to scrape followings
def scrape_followings(username):
    base_url = f"https://github.com/{username}"
    end_message = "That’s it. You’ve"
    return scrape_github_data(base_url, end_message, username, "following")

# Function to scrape followers
def scrape_followers(username):
    base_url = f"https://github.com/{username}"
    end_message = "That’s it. You’ve"
    return scrape_github_data(base_url, end_message, username, "followers")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/github', methods=['POST', 'GET', 'OPTIONS'])
def give_datas():
    username = request.args.get('username')

    isExisting = check_github_repo(username)
    if not isExisting:
        return jsonify({ 'status': 'failed' })

    # Scrape the "following" and "followers" pages
    following_html = scrape_followings(username)
    followers_html = scrape_followers(username)

    # Extract usernames from both HTMLs
    following_names = extract_usernames_from_html(following_html)
    followers_names = extract_usernames_from_html(followers_html)

    # Remove duplicates (if any) by converting to sets
    following_names = list(dict.fromkeys(following_names))
    followers_names = list(dict.fromkeys(followers_names))

    # Find users I follow but they don't follow back
    not_following_back = [user for user in following_names if user not in followers_names]

    # Find users who follow me, but I don't follow them back
    not_followed_by_me = [user for user in followers_names if user not in following_names]

    # Create response data
    response_data = {
        'status': 'success',
        'followers_count': len(followers_names),
        'following_count': len(following_names),
        'not_following_back': not_following_back, #[:10],  # Top 10 not following back
        'not_followed_by_me': not_followed_by_me #[:10]   # Top 10 not followed by me
    }

    return jsonify(response_data)


@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()
        

if __name__ == '__main__':
    app.run(debug=True)
