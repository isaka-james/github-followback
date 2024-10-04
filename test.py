import requests

def check_github_repo(github_url):
    try:
        # Send a request to the GitHub URL
        response = requests.get(github_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Repository exists.")
        else:
            # If the status code is not 200, check the title for "Page not found"
            if "Page not found" in response.text:
                print("Repository not found.")
            else:
                print("Repository exists, but another issue occurred.")
                
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
github_link = "https://github.com/isskjfdakaa"
check_github_repo(github_link)

