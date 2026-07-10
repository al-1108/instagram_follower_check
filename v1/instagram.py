import json

with open("followers_1.json") as f:
    followers_data = json.load(f)

with open("following.json") as f:
    following_data = json.load(f)

followers = set()
following = set()

for item in followers_data:
    followers.add(item["string_list_data"][0]["value"])


for item in following_data["relationships_following"]:
    following.add(item["title"])

not_following = set()

for followed in following:
    if followed not in followers:
        not_following.add(followed)

print()
print()

for username in not_following:
    print(f"{username}")

print(f"\n{len(not_following)} people don't follow you back")
