import json

from apscheduler.schedulers.background import BackgroundScheduler

from src.services.reddit_content_fetch_controller import (
    fetch_posts_last_xh,
    build_content_json,
)
from src.config import CONFIG


scheduler = BackgroundScheduler(timezone="UTC")


def run_scraper(hours_back: int):
    posts = fetch_posts_last_xh(hours_back)
    data = build_content_json(posts)
    print(json.dumps(data, indent=2))


def run_reddit_cronjob():
    if scheduler.running:
        return

    scheduler.add_job(
        run_scraper,
        trigger="interval",
        hours=CONFIG.FREQ_OF_DATA_RETRIEVAL,
        kwargs={"hours_back": CONFIG.HOURS_OF_CONTENT},
        id="archlinux_reddit_scraper",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    print("Reddit cron scheduler started")
