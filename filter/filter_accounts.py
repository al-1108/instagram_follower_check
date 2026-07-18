import json
import logging
import os
import random
import time
from datetime import date

logging.disable(logging.CRITICAL)

from instagrapi import Client
from instagrapi.exceptions import ClientNotFoundError, UserNotFound

MAX_FOLLOWERS = 20000
HALL_OF_SHAME_FILE = "hall_of_shame.json"
ACCOUNT_CACHE_FILE = "account_cache.json"
USE_ACCOUNT_CACHE = True  # toggle to False to re-check every account via the API instead of using cached results

with open("followers_1.json") as f:
    followers_data = json.load(f)

with open("following.json") as f:
    following_data = json.load(f)

if os.path.exists(HALL_OF_SHAME_FILE):
    with open(HALL_OF_SHAME_FILE) as f:
        hall_of_shame = json.load(f)
else:
    hall_of_shame = {}

if USE_ACCOUNT_CACHE and os.path.exists(ACCOUNT_CACHE_FILE):
    with open(ACCOUNT_CACHE_FILE) as f:
        account_cache = json.load(f)
else:
    account_cache = {}

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
cache_hits = 0
for username in not_following_back:
    cached = account_cache.get(username) if USE_ACCOUNT_CACHE else None
    if cached and cached["status"] == "celebrity":
        print(f"  (skipping {username} - {cached['followers']:,} followers) [cached]")
        cache_hits += 1
        continue
    if cached and cached["status"] == "deleted":
        print(f"  (skipping {username} - deleted account) [cached]")
        cache_hits += 1
        continue

    try:
        info = cl.user_info_by_username(username)
        if info.follower_count >= MAX_FOLLOWERS:
            print(f"  (skipping {username} - {info.follower_count:,} followers)")
            account_cache[username] = {
                "status": "celebrity",
                "followers": info.follower_count,
                "following": info.following_count,
            }
        else:
            results.append((username, [info.follower_count, info.following_count]))
            hall_of_shame[username] = {
                "followers": info.follower_count,
                "following": info.following_count,
                "date_added": hall_of_shame.get(username, {}).get("date_added", str(date.today())),
            }
            account_cache.pop(username, None)
    except (UserNotFound, ClientNotFoundError, KeyError):
        print(f"  (skipping {username} - deleted account)")
        account_cache[username] = {"status": "deleted"}
    except Exception as e:
        print(f"  (couldn't check {username}: {e})")
    time.sleep(random.uniform(500, 1000) / 1000)
    # DONT REMOVE THE ABOVE
    # it prevents instagram from blocking your account for too many requests

elapsed = time.time() - start_time

with open(HALL_OF_SHAME_FILE, "w") as f:
    json.dump(hall_of_shame, f, indent=2, sort_keys=True)

if USE_ACCOUNT_CACHE:
    with open(ACCOUNT_CACHE_FILE, "w") as f:
        json.dump(account_cache, f, indent=2, sort_keys=True)
    if cache_hits:
        print(f"\n{cache_hits} accounts skipped instantly using cached data from {ACCOUNT_CACHE_FILE}")

print(f"\n{len(results)} people don't follow you back\n")
for username, count in results:
    print(f"{username} ({count[0]:,} followers, {count[1]:,} following)")
    if count[0]/count[1] > 1.5:
        print(f"this person has a high following/follower ratio, they may also be an influencer")
    print()

if hall_of_shame:
    print(f"hall of shame ({len(hall_of_shame)} accounts total, saved to {HALL_OF_SHAME_FILE}):\n")
    for username, info in sorted(hall_of_shame.items()):
        print(f"{username} ({info['followers']:,} followers, since {info['date_added']})")
    print()

print(f"done in {int(elapsed // 60)}m {int(elapsed % 60)}s\n")
