
import asyncio
from datetime import datetime, timedelta
from twikit import Client
from src.hetzner_ip_manager import HetznerIPManager


class TwikitFetcher:
    def __init__(self, account_index: int, username: str, password: str):
        self.account_index = account_index
        self.username = username
        self.password = password

        self.hetzner_manager = HetznerIPManager()
        fip_id = self.hetzner_manager.create_floating_ip_if_needed(account_index)
        ip_addr = self.hetzner_manager.get_ip_for_account(account_index)
        print(f"[TwikitFetcher] Using Hetzner Floating IP {fip_id} / IP={ip_addr} for account {account_index}")

        self.client = Client()

    async def login(self):
        try:
            self.client.username = self.username
            self.client.password = self.password
            await self.client.login()
            print(f"[Fetcher] Account {self.account_index} logged in.")
        except Exception as e:
            print(f"[Fetcher] login failed: {e}")

    async def fetch_latest_tweets_12h(self, target_username: str):
        recent_tweets = []
        try:
            user = await self.client.get_user(username=target_username)
            if not user:
                print(f"[Fetcher] User {target_username} not found")
                return []
                
            tweets = await self.client.get_tweets(user.id, limit=50)
            cutoff_time = datetime.utcnow() - timedelta(hours=12)

            for tweet in tweets:
                tweet_dict = tweet.to_dict() if hasattr(tweet, 'to_dict') else tweet.__dict__
                
                created_at = tweet.created_at if hasattr(tweet, 'created_at') else None
                if created_at:
                    dt_utc = created_at.replace(tzinfo=None) if hasattr(created_at, 'replace') else created_at
                    
                    if dt_utc > cutoff_time:
                        recent_tweets.append(tweet_dict)
        except Exception as e:
            print(f"[Fetcher] fetch_latest_tweets_12h error for {target_username}: {e}")

        return recent_tweets
