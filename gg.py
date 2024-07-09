import requests
import time
import schedule

def display_banner():
    banner = """
    ***********************************************
    *                                             *
    *            Get Games by masbagus            *
    *                                             *
    *  GitHub: https://github.com/masbagusyutl    *
    *                                             *
    ***********************************************
    """
    print(banner)

def visit_url(account_number):
    claim_url = f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/account/{account_number}/claim"
    try:
        response = requests.put(claim_url)  # Use PUT method
        if response.status_code == 200:
            print(f"Successfully Claim")
        else:
            print(f"Failed to Claim, status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def complete_task(account_number):
    task_urls = [
        f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/tasks/{account_number}/complete/4",
        f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/tasks/{account_number}/complete/5",
        f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/tasks/{account_number}/complete/6",
        f"https://dolphin-app-2-qkmuv.ondigitalocean.app/api/tasks/{account_number}/complete/8"
    ]
    
    for i, task_url in enumerate(task_urls, start=1):
        try:
            response = requests.put(task_url)
            if response.status_code == 200:
                print(f"Task {i}: Successfully")
            else:
                print(f"Task {i}: Failed to complete task, status code: {response.status_code}")
        except Exception as e:
            print(f"Task {i}: An error occurred: {e}")

def countdown_timer(hours):
    total_seconds = hours * 3600
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        hrs, mins = divmod(mins, 60)
        time_format = f'{hrs:02}:{mins:02}:{secs:02}'
        print(f'Countdown: {time_format}', end='\r')
        time.sleep(1)
        total_seconds -= 1
    print()

def job(complete_task_enabled):
    # Read account numbers from file
    with open('data.txt', 'r') as file:
        account_numbers = file.read().splitlines()
    
    total_accounts = len(account_numbers)
    print(f"Total account numbers in file: {total_accounts}")

    for index, account_number in enumerate(account_numbers, start=1):
        print(f"Processing account {index}/{total_accounts}: {account_number}")
        visit_url(account_number)
        if complete_task_enabled:
            complete_task(account_number)
        time.sleep(2)  # Adding a short delay between requests

if __name__ == "__main__":
    display_banner()
    
    # Ask user if they want to enable complete_task feature
    complete_task_enabled = input("Do you want to enable the complete_task feature? (yes/no): ").strip().lower() == 'yes'

    # Schedule the job every 6 hours
    schedule.every(6).hours.do(job, complete_task_enabled=complete_task_enabled)

    # Initial run
    job(complete_task_enabled)

    # Keep the script running with countdown
    while True:
        schedule.run_pending()
        countdown_timer(6)  # Countdown for 6 hours
