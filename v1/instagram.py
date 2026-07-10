import json

with open("followers_1.json") as f:
    followers_data = json.load(f)

with open("following.json") as f:
    following_data = json.load(f)

not_following_back = set()

for item in following_data["relationships_following"]:
    not_following_back.add(item["title"])

# for item in followers_data:
#     not_following.add(item["string_list_data"][0]["value"])

for item in followers_data:
    if item["string_list_data"][0]["value"] in not_following_back:
        not_following_back.remove(item["string_list_data"][0]["value"])

# for item in following_data["relationships_following"]:
#     if item["title"] in not_following:
#         not_following.remove(item["title"])

print()
print()

for username in not_following_back:
    print(f"{username}")

print(f"\n{len(not_following_back)} people don't follow you back\n")
