import os
import sys
from dotenv import load_dotenv

load_dotenv(dotenv_path="./config/.env")

sys.path.append(os.path.abspath("./src"))

from src.accounts_config import AccountStateManager
from src.hetzner_ip_manager import HetznerIPManager
from src.twitter_post import TwitterPostClient

def test_account_state():
    print("Testing AccountStateManager...")
    state_manager = AccountStateManager()
    print(f"Account 1 part number: {state_manager.get_part_number(1)}")
    state_manager.increment_part_number(1)
    print(f"Account 1 part number after increment: {state_manager.get_part_number(1)}")
    print("AccountStateManager test completed.")

def test_hetzner_ip():
    print("Testing HetznerIPManager...")
    ip_manager = HetznerIPManager()
    print("HetznerIPManager initialized.")
    print("HetznerIPManager test completed.")

def test_twitter_post():
    print("Testing TwitterPostClient...")
    try:
        client = TwitterPostClient(1)
        print("TwitterPostClient initialized.")
    except Exception as e:
        print(f"Error initializing TwitterPostClient: {e}")
    print("TwitterPostClient test completed.")

if __name__ == "__main__":
    print("Starting functionality tests...")
    test_account_state()
    test_hetzner_ip()
    test_twitter_post()
    print("All tests completed.")
