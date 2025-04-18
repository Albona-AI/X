
import os
import tweepy
from accounts_config import AccountStateManager
from hetzner_ip_manager import HetznerIPManager


class TwitterPostClient:
    def __init__(self, account_index: int):
        self.account_index = account_index
        self.state_manager = AccountStateManager()

        self.hetzner_manager = HetznerIPManager()
        fip_id = self.hetzner_manager.create_floating_ip_if_needed(account_index)
        ip_addr = self.hetzner_manager.get_ip_for_account(account_index)
        print(f"[TwitterPostClient] Using Hetzner Floating IP {fip_id} / IP={ip_addr} for account {account_index}")

        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_KEY_SECRET")
        access_token = os.getenv(f"TWITTER_ACCESS_TOKEN_{account_index}")
        access_secret = os.getenv(f"TWITTER_ACCESS_TOKEN_SECRET_{account_index}")
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)

        self.api = tweepy.API(auth)

    def post_weather_tweet(self):
        part_num = self.state_manager.get_part_number(self.account_index)
        text = f"今日もいい天気だ！！ part{part_num}"

        try:
            status = self.api.update_status(status=text)
            print(f"[Account {self.account_index}] Posted: {text} (ID={status.id})")
            self.state_manager.increment_part_number(self.account_index)
            return status.id
        except Exception as e:
            print(f"[Account {self.account_index}] Post failed: {e}")
            return None
