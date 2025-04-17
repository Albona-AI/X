
import os
import asyncio
from twikit import Client
from hetzner_ip_manager import HetznerIPManager


class TwikitActions:
    def __init__(self, account_index: int):
        self.account_index = account_index
        self.username = os.getenv(f"TWIKIT_USERNAME_{account_index}")
        self.password = os.getenv(f"TWIKIT_PASSWORD_{account_index}")

        self.hetzner_manager = HetznerIPManager()
        fip_id = self.hetzner_manager.create_floating_ip_if_needed(account_index)
        ip_addr = self.hetzner_manager.get_ip_for_account(account_index)
        print(f"[TwikitActions] Using Hetzner Floating IP {fip_id} / IP={ip_addr} for account {account_index}")

        self.client = Client()

    async def login(self):
        try:
            self.client.username = self.username
            self.client.password = self.password
            await self.client.login()
            print(f"[TwikitActions] Account {self.account_index} logged in.")
        except Exception as e:
            print(f"[TwikitActions] Account {self.account_index} login failed: {e}")

    async def like_tweet(self, tweet_id: str):
        try:
            await self.client.favorite_tweet(tweet_id)
            print(f"[TwikitActions] Account {self.account_index} liked {tweet_id}")
        except Exception as e:
            print(f"like_tweet error: {e}")

    async def retweet_tweet(self, tweet_id: str):
        try:
            await self.client.retweet(tweet_id)
            print(f"[TwikitActions] Account {self.account_index} retweeted {tweet_id}")
        except Exception as e:
            print(f"retweet_tweet error: {e}")

    async def bookmark_tweet(self, tweet_id: str):
        try:
            await self.client.bookmark_tweet(tweet_id)
            print(f"[TwikitActions] Account {self.account_index} bookmarked {tweet_id}")
        except Exception as e:
            print(f"bookmark_tweet error: {e}")

    async def reply_tweet(self, tweet_id: str, text: str):
        try:
            await self.client.create_tweet(text=text, reply_to=tweet_id)
            print(f"[TwikitActions] Account {self.account_index} replied '{text}' to {tweet_id}")
        except Exception as e:
            print(f"reply_tweet error: {e}")
