# instagram follower check

Find out who doesn't follow you back.

two versions:

- `v1/` - basic list, no login needed, fast, includes celebrities and deleted accounts
- `filter/` - skips celebrities (20k+ followers) and deleted accounts, shows follower counts, flags possible influencers. needs your login

## setup

1. get your data: instagram → settings → accounts center → download your information → followers and following. pick **JSON** and **All time** 
2. drop `followers_1.json` and `following.json` into the version folder you're using
3. if you're using the filter version, set up the venv (from the repo root):

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## run

```
cd v1
python3 instagram.py
```

or

```
source .venv/bin/activate   # if not already active
cd filter
python3 filter_accounts.py
```

the filter one asks for your instagram login (not saved anywhere) and can take a while (for instance, an account with 200 followers and following would take around a minute) to run.

don't spam the filter version - it hits instagram's api through your account and too many runs can get you rate limited. you could log in with a burner account instead to keep your main safe (the lookups work from any account) - just don't use a brand new burner, let it age a bit with a profile pic and some normal activity or instagram will flag it fast.

## config

`MAX_FOLLOWERS` at the top of `filter_accounts.py` sets the celebrity cutoff - anyone with more followers than this gets skipped. default is 20000, raise or lower it to taste.

