# -----------------------------------------------------------------------------
# READ ME
#
# This is a pretty primitive set of functions, the purpose of which is to
# generate a CSV file containing all of your followers/following and their
# profile data. It's assumed that after generating this you will use a CSV
# viewer like Excel/Numbers/Google Sheets to sort, filter, and analyze the
# data. Bon Voyage and enjoy.
#
# INSTRUCTIONS FOR USE:
#
# First, replace the value of `actor` below with your handle.
# Then, from the command line, run the file using python3, e.g.:
# `python bluesky_follower_info.py`
#
# The data collection will take several minutes, depending on how many
# followers/following you have, so let it run. When it's done it will
# spit out a file called `all_related.csv` with your people in it.
# -----------------------------------------------------------------------------


import requests
import csv


actor = "PUT_YOUR_HANDLE_HERE.bsky.social"


def get_all_followers(handle):
    followers = []
    cursor = None

    while True:
        followers_resp = requests.get(
            f"https://public.api.bsky.app/xrpc/app.bsky.graph.getFollowers?actor={handle}&limit=100&cursor={cursor}"
        ).json()

        cursor = followers_resp.get("cursor")
        followers += followers_resp["followers"]

        if cursor is None:
            break

    followers_dict = {f["handle"]: f for f in followers}
    return followers_dict


def get_all_follows(handle):
    follows = []
    cursor = None

    while True:
        follows_resp = requests.get(
            f"https://public.api.bsky.app/xrpc/app.bsky.graph.getfollows?actor={handle}&limit=100&cursor={cursor}"
        ).json()

        cursor = follows_resp.get("cursor")
        follows += follows_resp["follows"]

        if cursor is None:
            break

    follows_dict = {f["handle"]: f for f in follows}

    return follows_dict


def get_non_mutuals(handle):
    followers = get_all_followers(handle)
    follows = get_all_follows(handle)

    follows_handles = set(follows.keys())
    followers_handles = set(followers.keys())

    followers_i_do_not_follow = followers_handles - follows_handles
    not_following = {handle: followers[handle] for handle in followers_i_do_not_follow}

    follows_who_do_not_follow_me = follows_handles - followers_handles
    not_following_me = {
        handle: follows[handle] for handle in follows_who_do_not_follow_me
    }

    return not_following, not_following_me


def fetch_profile(handle):
    profile = requests.get(
        f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={handle}"
    ).json()

    return profile


def save_profiles_to_csv(profiles, file_name):
    data = [profiles[0].keys(), *[profile.values() for profile in profiles]]

    with open(f"{file_name}.csv", "w") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "handle",
                "followedByMe",
                "followsMe",
                "followersCount",
                "followsCount",
                "postsCount",
                "displayName",
                "createdAt",
                "description",
                "associated",
                "avatar",
                "banner",
                "did",
                "indexedAt",
                "labels",
                "pinnedPost",
            ],
        )
        writer.writeheader()
        writer.writerows(profiles)


def fetch_all_related(handle):
    followers = get_all_followers(handle)
    follows = get_all_follows(handle)

    profiles = dict()

    # TODO: multithreading would make this faster
    for handle in followers.keys():
        profile = fetch_profile(handle)
        profiles[handle] = profile

    for handle in follows.keys():
        if profiles.get(handle) is None:
            profile = fetch_profile(handle)
            profiles[handle] = profile

    for handle in profiles.keys():
        profiles[handle]["followsMe"] = handle in followers
        profiles[handle]["followedByMe"] = handle in follows

    save_profiles_to_csv(list(profiles.values()), "all_related")
