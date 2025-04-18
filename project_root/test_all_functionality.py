import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv(dotenv_path="./config/.env")

sys.path.append(os.path.abspath("./src"))

from src.accounts_config import AccountStateManager
from src.hetzner_ip_manager import HetznerIPManager
from src.twitter_post import TwitterPostClient
from src.twikit_actions import TwikitActions
from src.twikit_fetch import TwikitFetcher
from src.ai_text_generator import generate_comment_text

def test_twitter_post():
    print("\n=== Testing Twitter Post Functionality ===")
    for idx in [1, 2, 3]:
        try:
            client = TwitterPostClient(idx)
            print(f"TwitterPostClient for account {idx} initialized.")
            tweet_id = client.post_weather_tweet()
            if tweet_id:
                print(f"Successfully posted tweet with ID: {tweet_id}")
            else:
                print(f"Failed to post tweet for account {idx}")
        except Exception as e:
            print(f"Error with TwitterPostClient for account {idx}: {e}")
    print("Twitter Post test completed.")

async def test_twikit_actions():
    print("\n=== Testing Twikit Actions Functionality ===")
    actions = []
    for idx in [1, 2, 3]:
        try:
            action = TwikitActions(idx)
            print(f"TwikitActions for account {idx} initialized.")
            await action.login()
            actions.append(action)
        except Exception as e:
            print(f"Error initializing TwikitActions for account {idx}: {e}")
    
    sample_tweet_id = "1234567890"
    for action in actions:
        try:
            await action.like_tweet(sample_tweet_id)
            await action.retweet_tweet(sample_tweet_id)
            await action.bookmark_tweet(sample_tweet_id)
            comment = generate_comment_text()
            await action.reply_tweet(sample_tweet_id, comment)
        except Exception as e:
            print(f"Error with Twikit actions: {e}")
    
    print("Twikit Actions test completed.")

async def test_twikit_fetch():
    print("\n=== Testing Twikit Fetch Functionality ===")
    for idx in [1, 2, 3]:
        try:
            username = os.getenv(f"TWIKIT_USERNAME_{idx}")
            password = os.getenv(f"TWIKIT_PASSWORD_{idx}")
            fetcher = TwikitFetcher(idx, username, password)
            print(f"TwikitFetcher for account {idx} initialized.")
            await fetcher.login()
            
            target_user = os.getenv("TWIKIT_USERNAME_1")
            tweets = await fetcher.fetch_latest_tweets_12h(target_user)
            print(f"Fetched {len(tweets)} tweets from {target_user}")
        except Exception as e:
            print(f"Error with TwikitFetcher for account {idx}: {e}")
    print("Twikit Fetch test completed.")

def test_hetzner_ip():
    print("\n=== Testing Hetzner IP Manager ===")
    try:
        ip_manager = HetznerIPManager()
        print("HetznerIPManager initialized.")
        
        for idx in [1, 2, 3]:
            fip_id = ip_manager.create_floating_ip_if_needed(idx)
            ip_addr = ip_manager.get_ip_for_account(idx)
            print(f"Account {idx}: Floating IP ID={fip_id}, IP={ip_addr}")
    except Exception as e:
        print(f"Error with HetznerIPManager: {e}")
    print("Hetzner IP Manager test completed.")

async def run_tests():
    print("Starting comprehensive functionality tests...")
    
    state_manager = AccountStateManager()
    print("\n=== Testing Account State Manager ===")
    for idx in [1, 2, 3]:
        print(f"Account {idx} part number: {state_manager.get_part_number(idx)}")
    print("Account State Manager test completed.")
    
    test_hetzner_ip()
    
    test_twitter_post()
    
    await test_twikit_actions()
    
    await test_twikit_fetch()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    asyncio.run(run_tests())
