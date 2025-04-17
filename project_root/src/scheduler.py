
import schedule
import time
import os
import asyncio


from twitter_post import TwitterPostClient
from twikit_actions import TwikitActions
from twikit_fetch import TwikitFetcher


ACCOUNT_INDICES = [1, 2, 3]


def job_post_once_a_day():
    """
    Post from all accounts daily at 08:00
    """
    for idx in ACCOUNT_INDICES:
        poster = TwitterPostClient(idx)
        poster.post_weather_tweet()


def get_comment_text():
    """
    May be extended to AI generation in the future.
    Currently fixed as "いいね！".
    """
    return "いいね！"


def job_interaction_12h():
    """
    At 0:00 & 12:00:
      - Fetch tweets posted in the last 12h
      - Like/RT/save/comment ("いいね！")
    """

    async def _interaction_flow():
        fetchers = []
        actions_list = []
        for idx in ACCOUNT_INDICES:
            username = os.getenv(f"TWIKIT_USERNAME_{idx}")
            password = os.getenv(f"TWIKIT_PASSWORD_{idx}")
            fetcher = TwikitFetcher(idx, username, password)
            action = TwikitActions(idx)
            fetchers.append(fetcher)
            actions_list.append(action)

        for f in fetchers:
            await f.login()
        for a in actions_list:
            await a.login()

        for i, fetcher in enumerate(fetchers):
            all_tweets = []
            for target_idx in ACCOUNT_INDICES:
                target_user = os.getenv(f"TWIKIT_USERNAME_{target_idx}")
                tweets = await fetcher.fetch_latest_tweets_12h(target_user)
                all_tweets.extend(tweets)

            unique_map = {}
            for t in all_tweets:
                tid = t.get("id_str")
                if tid:
                    unique_map[tid] = t
            unique_tweets = list(unique_map.values())

            action_obj = actions_list[i]
            for tw in unique_tweets:
                tid = tw["id_str"]
                await action_obj.like_tweet(tid)
                await action_obj.retweet_tweet(tid)
                await action_obj.bookmark_tweet(tid)
                c_text = get_comment_text()
                await action_obj.reply_tweet(tid, c_text)

    asyncio.run(_interaction_flow())


def start_scheduler():
    print("Running initial post job for testing...")
    job_post_once_a_day()
    
    print("Running initial interaction job for testing...")
    job_interaction_12h()
    
    schedule.every().day.at("08:00").do(job_post_once_a_day)
    schedule.every().day.at("00:00").do(job_interaction_12h)
    schedule.every().day.at("12:00").do(job_interaction_12h)

    print("Scheduler set up. Waiting for scheduled tasks...")
    while True:
        schedule.run_pending()
        time.sleep(1)
