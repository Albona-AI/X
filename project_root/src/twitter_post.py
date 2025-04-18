
import os
import tweepy
from src.accounts_config import AccountStateManager
from src.hetzner_ip_manager import HetznerIPManager


class TwitterPostClient:
    def __init__(self, account_index: int):
        self.account_index = account_index
        self.state_manager = AccountStateManager()

        self.hetzner_manager = HetznerIPManager()
        fip_id = self.hetzner_manager.create_floating_ip_if_needed(account_index)
        ip_addr = self.hetzner_manager.get_ip_for_account(account_index)
        print(f"[TwitterPostClient] Using Hetzner Floating IP {fip_id} / IP={ip_addr} for account {account_index}")

        api_key = os.getenv(f"TWITTER_API_KEY_{account_index}")
        api_secret = os.getenv(f"TWITTER_API_KEY_SECRET_{account_index}")
        access_token = os.getenv(f"TWITTER_ACCESS_TOKEN_{account_index}")
        access_secret = os.getenv(f"TWITTER_ACCESS_TOKEN_SECRET_{account_index}")
        
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )

    def post_weather_tweet(self):
        part_num = self.state_manager.get_part_number(self.account_index)
        text = f"今日もいい天気だ！！ part{part_num}"

        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            print(f"[Account {self.account_index}] Posted: {text} (ID={tweet_id})")
            self.state_manager.increment_part_number(self.account_index)
            return tweet_id
        except Exception as e:
            print(f"[Account {self.account_index}] Post failed: {e}")
            return None
