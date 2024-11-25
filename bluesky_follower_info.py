import requests
from concurrent.futures import ThreadPoolExecutor

actor = "1t2ls.bsky.social"


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


def print_sorted_list_by_follower_count(
    followers, *, invert=False, ignore_dubiousness=False
):
    handle_followerCount_followingCount = list()

    def fetch_follower_count(handle):
        # print(f"fetching... {handle}")
        profile = requests.get(
            f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={handle}"
        ).json()
        handle_followerCount_followingCount.append(
            (handle, profile["followersCount"], profile["followsCount"])
        )

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(fetch_follower_count, followers)

    handle_followerCount_followingCount.sort(
        reverse=(not invert), key=lambda flwr: flwr[1]
    )

    print(
        "{: <60}".format("PROFILE LINK")
        + "{: <12}".format("FOLLOWERS")
        + "{: <12}".format("FOLLOWING")
    )

    for handle, followerCount, followingCount in handle_followerCount_followingCount[
        :300
    ]:
        is_dubious = (not ignore_dubiousness) and (followerCount / followingCount) < 2
        if not is_dubious:

            print(
                "{: <60}".format("https://bsky.app/profile/" + handle)
                + "{: <12}".format(followerCount)
                + "{: <12}".format(followingCount)
            )


not_following, not_following_me = get_non_mutuals(actor)


print("\n\n\n\nTHESE ARE YOUR TOP FOLLOWERS BY FOLLOW COUNT")
print_sorted_list_by_follower_count(get_all_followers(actor).keys())

print("\n\n\n\nYOU DO NOT FOLLOW THESE PEOPLE BACK")
print_sorted_list_by_follower_count(not_following.keys())

print("\n\n\n\nTHESE PEOPLE DO NOT FOLLOW YOU BACK")
print_sorted_list_by_follower_count(not_following_me.keys(), ignore_dubiousness=True)
