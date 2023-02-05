import requests
import threading

with open("usernames.txt") as file:
    usernames = file.readlines()

not_found_usernames = []
lock = threading.Lock()

def check_username(username, index):
    url = f'https://api.chess.com/pub/player/{username}'
    response = requests.get(url)
    if response.status_code == 404:
        with lock:
            not_found_usernames.append(username)
            print(f"\033[32mUsername {username} is available!\033[0m ({len(usernames) - index - 1} usernames left to check, {(index + 1) / len(usernames) * 100:.2f}% done)")
    else:
        print(f"\033[31mUsername {username} is not available.\033[0m ({len(usernames) - index - 1} usernames left to check, {(index + 1) / len(usernames) * 100:.2f}% done)")

threads = []

for index, username in enumerate(usernames):
    username = username.strip()
    thread = threading.Thread(target=check_username, args=(username, index))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

with open("results.txt", "w") as file:
    for username in not_found_usernames:
        file.write(username + "\n")
