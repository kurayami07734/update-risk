import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from src.services.reddit_content_fetch_controller import (
    fetch_posts_last_xh,
    build_content_json,
)
from src.config import CONFIG
from src.controllers.data_extraction_controller import reddit_data_extraction

scheduler = BackgroundScheduler(timezone="UTC")


async def run_scraper_async(hours_back: int):
    posts = fetch_posts_last_xh(hours_back)
    # print(posts)
    data = build_content_json(posts)
    response = await reddit_data_extraction(data)
    print("Final Resp:",response)


def run_scraper(hours_back: int):
    asyncio.run(run_scraper_async(hours_back))


def run_reddit_cronjob():
    if scheduler.running:
        return

    scheduler.add_job(
        run_scraper,
        trigger="interval",
        # seconds=30,
        hours = 1,
        kwargs={"hours_back": CONFIG.HOURS_OF_CONTENT},
        id="archlinux_reddit_scraper",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    print("Reddit cron scheduler started")
