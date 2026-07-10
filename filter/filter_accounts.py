import json
import logging
import random
import time

logging.disable(logging.CRITICAL)

from instagrapi import Client
from instagrapi.exceptions import ClientNotFoundError, UserNotFound

MAX_FOLLOWERS = 20000

with open("followers_1.json") as f:
    followers_data = json.load(f)

with open("following.json") as f:
    following_data = json.load(f)

not_following_back = set()

for item in following_data["relationships_following"]:
    not_following_back.add(item["title"])

for item in followers_data:
    if item["string_list_data"][0]["value"] in not_following_back:
        not_following_back.remove(item["string_list_data"][0]["value"])
        
print(f"\nchecking {len(not_following_back)} accounts\n")

username = input("instagram username: ")
password = input("instagram password: ")

print(f"\nAuthenticating...")

cl = Client()
cl.login(username, password)

print(f"Starting to check... this may take a few minutes\n")
start_time = time.time()

results = []
for username in not_following_back:
    try:
        info = cl.user_info_by_username(username)
        if info.follower_count >= MAX_FOLLOWERS:
            print(f"  (skipping {username} - {info.follower_count:,} followers)")
        else:
            results.append((username, [info.follower_count, info.following_count]))
    except (UserNotFound, ClientNotFoundError, KeyError):
        print(f"  (skipping {username} - deleted account)")
    except Exception as e:
        print(f"  (couldn't check {username}: {e})")
    time.sleep(random.uniform(500, 1000) / 1000) 
    # DONT REMOVE THE ABOVE 
    # it prevents instagram from blocking your account for too many requests

elapsed = time.time() - start_time

print(f"\n{len(results)} people don't follow you back\n")
for username, count in results:
    print(f"{username} ({count[0]:,} followers, {count[1]:,} following)")
    if count[0]/count[1] > 1.5:
        print(f"this person has a high following/follower ratio, they may also be an influencer")
    print()
print(f"done in {int(elapsed // 60)}m {int(elapsed % 60)}s\n")
