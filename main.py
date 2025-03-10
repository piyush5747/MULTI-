import requests
import time
import json
import os

def clear_screen():
    os.system('clear')

def print_header():
    print("="*50)
    print("          MULTI COOKIES COMMENT SCRIPT")
    print("="*50)

def main():
    clear_screen()
    print_header()
    
    # User inputs
    post_id = input("Enter Facebook Post ID: ").strip()
    hater_name = input("Enter Hater's Name: ").strip()
    cookies_input = input("Enter the path of file containing JSON Cookies: ").strip()
    comment_file_path = input("Enter the path of file containing comments: ").strip()
    delay = int(input("Enter delay in seconds between comments: ").strip())

    # Validate files
    if not os.path.exists(cookies_input):
        print("Cookies file not found!")
        return
    if not os.path.exists(comment_file_path):
        print("Comments file not found!")
        return

    # Load cookies and comments
    try:
        with open(cookies_input, 'r') as f:
            cookies_list = json.load(f)
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return

    try:
        with open(comment_file_path, 'r') as f:
            comments = f.readlines()
    except Exception as e:
        print(f"Error loading comments: {e}")
        return

    # Posting comments
    for index, cookie in enumerate(cookies_list, start=1):
        print(f"\nUsing Cookie {index}/{len(cookies_list)}")
        session = requests.Session()
        session.cookies.update(cookie)

        for comment in comments:
            comment_text = comment.strip().replace("{hater_name}", hater_name)
            if not comment_text:
                continue

            payload = {
                "message": comment_text,
                "id": post_id
            }

            try:
                response = session.post("https://graph.facebook.com/v17.0/comments", data=payload)
                if response.status_code == 200:
                    print(f"Comment posted: {comment_text}")
                else:
                    print(f"Failed to post comment: {response.json()}")
            except Exception as e:
                print(f"Error posting comment: {e}")

            time.sleep(delay)

    print("\nAll comments have been posted.")

if __name__ == "__main__":
    main()