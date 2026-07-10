# instagram follower check

Find out who doesn't follow you back.

two versions:

- `v1/` - basic list, no login needed, fast, includes celebrities and deleted accounts
- `filter/` - skips celebrities (20k+ followers) and deleted accounts, shows follower counts, flags possible influencers. needs your login

## setup

1. get your data: instagram → settings → accounts center → download your information → followers and following. pick **JSON** and **All time** 
2. drop `followers_1.json` and `following.json` into the version folder you're using
3. if you're using the filter version: `pip3 install instagrapi`

## run

```
cd v1
python3 instagram.py
```

or

```
cd filter
python3 filter_accounts.py
```

the filter one asks for your instagram login (not saved anywhere) and can take a while (for instance, an account with 200 followers and following would take around a minute) to run.

don't spam the filter version - it hits instagram's api through your account and too many runs can get you rate limited.
