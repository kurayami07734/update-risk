import requests
import time
import json
from datetime import datetime, timezone
from src.utils.formatter import clean_text


SUBREDDIT = "archlinux"

HEADERS = {
    "User-Agent": "archlinux-json-scraper/1.0"
}




def fetch_posts_last_xh(hours):
    cutoff = datetime.now(timezone.utc).timestamp() - (hours * 3600)
    after = None
    posts = []

    while True:
        url = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit=100"
        if after:
            url += f"&after={after}"

        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()["data"]

        children = data["children"]
        if not children:
            break

        stop = False
        for child in children:
            post = child["data"]
            if post["created_utc"] >= cutoff:
                posts.append(post)
            else:
                stop = True
                break

        if stop:
            break

        after = data.get("after")
        if not after:
            break

        time.sleep(1)

    return posts


def extract_comments(children, lines, indent=""):
    for child in children:
        if child["kind"] != "t1":
            continue

        body = clean_text(child["data"].get("body"))
        if body:
            lines.append(f"{indent}- {body}")

        replies = child["data"].get("replies")
        if isinstance(replies, dict):
            extract_comments(
                replies["data"]["children"],
                lines,
                indent + "     "
            )


def fetch_post_content(post):
    url = f"https://www.reddit.com{post['permalink']}.json"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    post_data = data[0]["data"]["children"][0]["data"]
    comment_tree = data[1]["data"]["children"]

    lines = []

    time_str = datetime.fromtimestamp(
        post_data["created_utc"], tz=timezone.utc
    ).strftime("%Y-%m-%d %H:%M UTC")

    lines.append(time_str)
    lines.append(f" - {post_data['title']}")

    description = clean_text(post_data.get("selftext"))
    if description:
        lines.append("   Description:")
        lines.append(f"    {description}")

    if comment_tree:
        lines.append("   Comments:")
        extract_comments(comment_tree, lines)

    return {
        "content": "\n".join(lines)
    }



def build_content_json(posts):
    result = []

    for post in posts:
        result.append(fetch_post_content(post))
        time.sleep(1)

    return result
