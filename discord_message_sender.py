from config import CHANNEL_ID, SECOND_CHANNEL_ID, SUI_WALLET_ADDRESS, AUTHORIZATION_TOKENS

import requests
import json
import time
import schedule

class Colors:
    PINK = '\033[95m'
    RED = '\033[91m'
    RESET = '\033[0m'
combined_banner = """
         ,                 ██████╗ ██╗███╗   ██╗██╗  ██╗███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗
       .';                 ██╔══██╗██║████╗  ██║██║ ██╔╝██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝
   .-'` .'                 ██████╔╝██║██╔██╗ ██║█████╔╝ ███████╗███████║███████║██████╔╝█████╔╝ 
 ,`.-'-.`\\                 ██╔═══╝ ██║██║╚██╗██║██╔═██╗ ╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗ 
; /     '-'                ██║     ██║██║ ╚████║██║  ██╗███████║██║  ██║██║  ██║██║  ██║██║  ██╗
| \\       ,-,              ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
\\  '-.__   )_`'._     
 '.     ```      ``'--._          
.-' ,                   `'-.   
 '-'`-._           ((   o   )    
        `'--....(`- ,__..--'     
                 '-'`            
    """

def print_banner():
    for line in combined_banner.split('\n'):
        print(f"{Colors.PINK}{line}{Colors.RESET}")
def run_bot():
    start_time = time.time()
    for auth_token in AUTHORIZATION_TOKENS:
        message_content = f"!faucet {SUI_WALLET_ADDRESS}"
        print(f"{Colors.PINK}Sending message with token: {auth_token}{Colors.RESET}")
        print(f"{Colors.PINK}Message to send: {message_content}{Colors.RESET}")

        for channel_id in [CHANNEL_ID, SECOND_CHANNEL_ID]:
            try:
                if not auth_token or not channel_id or not SUI_WALLET_ADDRESS:
                    print("Authorization token, channel ID, and SUI Wallet Address cannot be empty.")
                else:
                    send_discord_message(auth_token, channel_id, message_content)
            except requests.exceptions.HTTPError as errh:
                print(f"{Colors.RED}HTTP 429 Error: Slowmode limit. Retry after: {errh.response.json().get('retry_after', 0) / 1000:.2f} seconds{Colors.RESET}")
                continue
            except requests.exceptions.RequestException as err:
                print(f"{Colors.RED}Request Error: {err}{Colors.RESET}")
                continue

        time.sleep(3)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{Colors.PINK}Bot run completed in: {elapsed_time:.2f} seconds{Colors.RESET}")

def schedule_bot(interval):
    run_bot()
    hours, minutes = map(int, interval.split(':'))
    total_seconds = hours * 3600 + minutes * 60
    schedule.every(total_seconds).seconds.do(run_bot)
    while True:
        print(f"{Colors.PINK}Next run in: {hours} hours {minutes} minutes{Colors.RESET}")
        for remaining in range(total_seconds, 0, -1):
            h, remainder = divmod(remaining, 3600)
            m, s = divmod(remainder, 60)
            print(f"{Colors.PINK}Time until next run: {h}h {m}m {s}s{Colors.RESET}", end='\r')
            time.sleep(1)
        schedule.run_pending()

def send_discord_message(token, channel_id, message):
    """
    Sends a message to a specific Discord channel using an authorization token.

    WARNING: Using user authorization tokens (self-bots) is against Discord's
    Terms of Service and can result in your account being banned.
    Use this script at your own risk. It is recommended to use official
    Discord bot accounts and libraries for automation.
    """
    
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    payload = {
        "content": message
    }
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" # Common user agent
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print(f"{Colors.PINK}Message sent successfully to channel {channel_id}!{Colors.RESET}")
        # print(f"Response: {response.json()}") # Avoid printing if sensitive
    except requests.exceptions.HTTPError as errh:
        print(f"{Colors.RED}HTTP 429 Error: Slowmode limit. Retry after: {errh.response.json().get('retry_after', 0) / 1000:.2f} seconds{Colors.RESET}")
        print(f"{Colors.RED}Response status code: {errh.response.status_code}{Colors.RESET}")
        print(f"{Colors.RED}Response content: {errh.response.content.decode()}{Colors.RESET}")
    except requests.exceptions.ConnectionError as errc:
        print(f"{Colors.RED}Error Connecting: {errc}{Colors.RESET}")
    except requests.exceptions.Timeout as errt:
        print(f"{Colors.RED}Timeout Error: {errt}{Colors.RESET}")
    except requests.exceptions.RequestException as err:
        print(f"{Colors.RED}Oops: Something Else: {err}{Colors.RESET}")

if __name__ == "__main__":
    print_banner()
    print(f"{Colors.PINK}Discord Message Sender (using Authorization Token){Colors.RESET}")
    print(f"{Colors.PINK}========================================{Colors.RESET}")
    print(f"{Colors.PINK}Warning: Using self-bots can result in a ban.{Colors.RESET}")
    print(f"{Colors.PINK}Consider using an official Discord Bot.{Colors.RESET}")
    print(f"{Colors.PINK}========================================{Colors.RESET}")

    while True:
        print(f"{Colors.PINK}1. Run Bot Now{Colors.RESET}")
        print(f"{Colors.PINK}2. Schedule Bot{Colors.RESET}")
        print(f"{Colors.PINK}3. Cancel{Colors.RESET}")
        choice = input(f"{Colors.PINK}Enter your choice: {Colors.RESET}")

        if choice == '1':
            run_bot()
        elif choice == '2':
            interval = input(f"{Colors.PINK}Enter the interval in hours:minutes (e.g., 1:30): {Colors.RESET}")
            schedule_bot(interval)
        elif choice == '3':
            print(f"{Colors.PINK}Cancelled.{Colors.RESET}")
            break
        else:
            print(f"{Colors.PINK}Invalid choice.{Colors.RESET}")
